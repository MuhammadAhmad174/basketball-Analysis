import os
import argparse
import pandas as pd
from utils import read_video, save_video
from trackers import PlayerTracker, BallTracker
from team_assigner import TeamAssigner
from court_keypoint_detector import CourtKeypointDetector
from ball_aquisition import BallAquisitionDetector
from pass_and_interception_detector import PassAndInterceptionDetector
from tactical_view_converter import TacticalViewConverter
from speed_and_distance_calculator import SpeedAndDistanceCalculator
from drawers import (
    PlayerTracksDrawer, 
    BallTracksDrawer,
    CourtKeypointDrawer,
    TeamBallControlDrawer,
    FrameNumberDrawer,
    PassInterceptionDrawer,
    TacticalViewDrawer,
    SpeedAndDistanceDrawer
)
from configs import(
    STUBS_DEFAULT_PATH,
    PLAYER_DETECTOR_PATH,
    BALL_DETECTOR_PATH,
    COURT_KEYPOINT_DETECTOR_PATH,
    OUTPUT_VIDEO_PATH
)

def parse_args():
    parser = argparse.ArgumentParser(description='Basketball Video Analysis')
    parser.add_argument('input_video', type=str, help='Path to input video file')
    parser.add_argument('--output_video', type=str, default=OUTPUT_VIDEO_PATH, 
                        help='Path to output video file')
    parser.add_argument('--stub_path', type=str, default=STUBS_DEFAULT_PATH,
                        help='Path to stub directory')
    parser.add_argument('--export_csv', action='store_true',
                        help='Export analysis data to CSV for game analysis pipeline')
    parser.add_argument('--csv_output_dir', type=str, default='csv_output',
                        help='Directory for CSV output files')
    parser.add_argument('--run_analysis', action='store_true',
                        help='Run game analysis pipeline after video processing')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Read Video
    video_frames = read_video(args.input_video)
    
    ## Initialize Tracker
    player_tracker = PlayerTracker(PLAYER_DETECTOR_PATH)
    ball_tracker = BallTracker(BALL_DETECTOR_PATH)

    ## Initialize Keypoint Detector
    court_keypoint_detector = CourtKeypointDetector(COURT_KEYPOINT_DETECTOR_PATH)

    # Run Detectors
    player_tracks = player_tracker.get_object_tracks(video_frames,
                                       read_from_stub=True,
                                       stub_path=os.path.join(args.stub_path, 'player_track_stubs.pkl')
                                      )
    
    ball_tracks = ball_tracker.get_object_tracks(video_frames,
                                                 read_from_stub=True,
                                                 stub_path=os.path.join(args.stub_path, 'ball_track_stubs.pkl')
                                                )
    ## Run KeyPoint Extractor
    court_keypoints_per_frame = court_keypoint_detector.get_court_keypoints(video_frames,
                                                                    read_from_stub=True,
                                                                    stub_path=os.path.join(args.stub_path, 'court_key_points_stub.pkl')
                                                                    )

    # Remove Wrong Ball Detections
    ball_tracks = ball_tracker.remove_wrong_detections(ball_tracks)
    # Interpolate Ball Tracks
    ball_tracks = ball_tracker.interpolate_ball_positions(ball_tracks)
   

    # Assign Player Teams
    team_assigner = TeamAssigner()
    player_assignment = team_assigner.get_player_teams_across_frames(video_frames,
                                                                    player_tracks,
                                                                    read_from_stub=True,
                                                                    stub_path=os.path.join(args.stub_path, 'player_assignment_stub.pkl')
                                                                    )

    # Ball Acquisition
    ball_aquisition_detector = BallAquisitionDetector()
    ball_aquisition = ball_aquisition_detector.detect_ball_possession(player_tracks,ball_tracks)

    # Detect Passes
    pass_and_interception_detector = PassAndInterceptionDetector()
    passes = pass_and_interception_detector.detect_passes(ball_aquisition,player_assignment)
    interceptions = pass_and_interception_detector.detect_interceptions(ball_aquisition,player_assignment)

    # Tactical View
    tactical_view_converter = TacticalViewConverter(
        court_image_path="./images/basketball_court.png"
    )

    try:
        court_keypoints_per_frame = tactical_view_converter.validate_keypoints(court_keypoints_per_frame)
        tactical_player_positions = tactical_view_converter.transform_players_to_tactical_view(court_keypoints_per_frame,player_tracks)
    except (IndexError, AttributeError) as e:
        print(f"\n⚠️  Warning: Court keypoint validation failed: {e}")
        print("Continuing without tactical view transformation...")
        tactical_player_positions = {}

    # Speed and Distance Calculator
    speed_and_distance_calculator = SpeedAndDistanceCalculator(
        tactical_view_converter.width,
        tactical_view_converter.height,
        tactical_view_converter.actual_width_in_meters,
        tactical_view_converter.actual_height_in_meters
    )
    player_distances_per_frame = speed_and_distance_calculator.calculate_distance(tactical_player_positions)
    player_speed_per_frame = speed_and_distance_calculator.calculate_speed(player_distances_per_frame)

    # Draw output   
    # Initialize Drawers
    player_tracks_drawer = PlayerTracksDrawer()
    ball_tracks_drawer = BallTracksDrawer()
    court_keypoint_drawer = CourtKeypointDrawer()
    team_ball_control_drawer = TeamBallControlDrawer()
    frame_number_drawer = FrameNumberDrawer()
    pass_and_interceptions_drawer = PassInterceptionDrawer()
    tactical_view_drawer = TacticalViewDrawer()
    speed_and_distance_drawer = SpeedAndDistanceDrawer()

    ## Draw object Tracks
    output_video_frames = player_tracks_drawer.draw(video_frames, 
                                                    player_tracks,
                                                    player_assignment,
                                                    ball_aquisition)
    
    if len(output_video_frames) == 0:
        print("\n❌ Error: Player tracks drawer returned empty frames")
        output_video_frames = video_frames
    
    output_video_frames = ball_tracks_drawer.draw(output_video_frames, ball_tracks)

    ## Draw KeyPoints
    try:
        output_video_frames = court_keypoint_drawer.draw(output_video_frames, court_keypoints_per_frame)
    except Exception as e:
        print(f"\n⚠️  Warning: Court keypoint drawing failed: {e}")

    ## Draw Frame Number
    output_video_frames = frame_number_drawer.draw(output_video_frames)

    # Draw Team Ball Control
    output_video_frames = team_ball_control_drawer.draw(output_video_frames,
                                                        player_assignment,
                                                        ball_aquisition)

    # Draw Passes and Interceptions
    output_video_frames = pass_and_interceptions_drawer.draw(output_video_frames,
                                                             passes,
                                                             interceptions)
    
    # Speed and Distance Drawer
    try:
        output_video_frames = speed_and_distance_drawer.draw(output_video_frames,
                                                             player_tracks,
                                                             player_distances_per_frame,
                                                             player_speed_per_frame
                                                             )
    except Exception as e:
        print(f"\n⚠️  Warning: Speed and distance drawing failed: {e}")

    ## Draw Tactical View
    try:
        if len(tactical_player_positions) > 0:
            output_video_frames = tactical_view_drawer.draw(output_video_frames,
                                                            tactical_view_converter.court_image_path,
                                                            tactical_view_converter.width,
                                                            tactical_view_converter.height,
                                                            tactical_view_converter.key_points,
                                                            tactical_player_positions,
                                                            player_assignment,
                                                            ball_aquisition,
                                                            )
        else:
            print("\n⚠️  Skipping tactical view drawing (no tactical positions available)")
    except Exception as e:
        print(f"\n⚠️  Warning: Tactical view drawing failed: {e}")
        print("Continuing without tactical view overlay...")

    # Save video
    if len(output_video_frames) > 0:
        save_video(output_video_frames, args.output_video)
    else:
        print("\n❌ Error: No output frames generated. Video cannot be saved.")
        print("This might be due to issues with the video processing pipeline.")

    # Export CSV if requested
    if args.export_csv:
        csv_path = export_to_csv(
            args.input_video,
            args.csv_output_dir,
            player_tracks,
            ball_tracks,
            player_assignment,
            ball_aquisition,
            passes,
            interceptions,
            tactical_player_positions,
            player_distances_per_frame,
            player_speed_per_frame,
            video_frames
        )
        
        # Check if CSV has data
        if csv_path and os.path.exists(csv_path):
            import pandas as pd
            try:
                test_df = pd.read_csv(csv_path)
                if len(test_df) == 0:
                    print("\n⚠️  Warning: CSV file is empty. Skipping game analysis.")
                    csv_path = None
            except:
                print("\n⚠️  Warning: CSV file is invalid. Skipping game analysis.")
                csv_path = None
    else:
        csv_path = None
    
    # Run game analysis if requested
    if args.run_analysis:
        if not args.export_csv or csv_path is None:
            print("\n⚠️  Skipping game analysis: No valid CSV data available")
            print("Game analysis requires successful video processing and CSV export.")
        else:
            run_game_analysis(args.input_video, csv_path)

def export_to_csv(input_video, csv_output_dir, player_tracks, ball_tracks, 
                  player_assignment, ball_aquisition, passes, interceptions,
                  tactical_player_positions, player_distances_per_frame, 
                  player_speed_per_frame, video_frames):
    """Export all analysis data to CSV format."""
    print("\n" + "="*70)
    print("EXPORTING DATA TO CSV")
    print("="*70)
    
    # Get video name and create video-specific folder
    video_name = os.path.splitext(os.path.basename(input_video))[0]
    video_output_dir = os.path.join(csv_output_dir, video_name)
    os.makedirs(video_output_dir, exist_ok=True)
    
    # Single CSV file with all results
    csv_path = os.path.join(video_output_dir, f"{video_name}_complete_analysis.csv")
    
    # Build combined dataframe
    rows = []
    fps = 30  # Assuming 30 fps, adjust if needed
    
    for frame_num in range(len(video_frames)):
        timestamp = frame_num / fps
        
        # Get ball position
        ball_pos = None
        if frame_num in ball_tracks and 1 in ball_tracks[frame_num]:
            ball_bbox = ball_tracks[frame_num][1]
            ball_pos = ((ball_bbox[0] + ball_bbox[2]) / 2, (ball_bbox[1] + ball_bbox[3]) / 2)
        
        # Process each player
        if frame_num in player_tracks:
            for player_id, bbox in player_tracks[frame_num].items():
                # Basic info
                row = {
                    'frame_number': frame_num,
                    'timestamp': timestamp,
                    'player_id': player_id,
                    'bbox_x1': bbox[0],
                    'bbox_y1': bbox[1],
                    'bbox_x2': bbox[2],
                    'bbox_y2': bbox[3],
                }
                
                # Team assignment
                if frame_num in player_assignment and player_id in player_assignment[frame_num]:
                    row['team_id'] = player_assignment[frame_num][player_id]
                else:
                    row['team_id'] = None
                
                # Ball possession
                has_ball = False
                if frame_num in ball_aquisition and ball_aquisition[frame_num] == player_id:
                    has_ball = True
                row['has_ball'] = has_ball
                
                # Tactical position
                if frame_num in tactical_player_positions and player_id in tactical_player_positions[frame_num]:
                    tac_pos = tactical_player_positions[frame_num][player_id]
                    row['tactical_x'] = tac_pos[0]
                    row['tactical_y'] = tac_pos[1]
                else:
                    row['tactical_x'] = None
                    row['tactical_y'] = None
                
                # Speed
                if frame_num in player_speed_per_frame and player_id in player_speed_per_frame[frame_num]:
                    row['speed_speed_kmh'] = player_speed_per_frame[frame_num][player_id]
                else:
                    row['speed_speed_kmh'] = 0.0
                
                # Distance
                if frame_num in player_distances_per_frame and player_id in player_distances_per_frame[frame_num]:
                    row['distance_cumulative_distance_meters'] = player_distances_per_frame[frame_num][player_id]
                else:
                    row['distance_cumulative_distance_meters'] = 0.0
                
                # Ball position
                if ball_pos:
                    row['ball_x'] = ball_pos[0]
                    row['ball_y'] = ball_pos[1]
                else:
                    row['ball_x'] = None
                    row['ball_y'] = None
                
                rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(rows)
    
    # Check if we have data
    if len(df) == 0:
        print("\n⚠️  Warning: No player tracking data found. CSV will be empty.")
        print("This might happen if:")
        print("  - Video processing hasn't completed")
        print("  - No players were detected in the video")
        print("  - Stub files are missing or corrupted")
        df.to_csv(csv_path, index=False)
        return csv_path
    
    # Add pass and interception flags
    df['is_pass'] = False
    df['is_interception'] = False
    df['pass_team'] = None
    df['interception_team'] = None
    
    # Passes and interceptions are lists where index is frame number
    # Value is -1 (no event), 1 (team 1), or 2 (team 2)
    if len(passes) > 0:
        for frame_num in range(len(passes)):
            if passes[frame_num] != -1:
                mask = df['frame_number'] == frame_num
                df.loc[mask, 'is_pass'] = True
                df.loc[mask, 'pass_team'] = passes[frame_num]
    
    if len(interceptions) > 0:
        for frame_num in range(len(interceptions)):
            if interceptions[frame_num] != -1:
                mask = df['frame_number'] == frame_num
                df.loc[mask, 'is_interception'] = True
                df.loc[mask, 'interception_team'] = interceptions[frame_num]
    
    # Save to CSV
    df.to_csv(csv_path, index=False)
    print(f"\nCSV exported to: {csv_path}")
    print(f"Total rows: {len(df)}")
    print(f"Columns: {', '.join(df.columns)}")
    
    return csv_path

def run_game_analysis(input_video, csv_path):
    """Run the game analysis pipeline."""
    print("\n" + "="*70)
    print("RUNNING GAME ANALYSIS PIPELINE")
    print("="*70)
    
    try:
        from game_analysis.index import main as analysis_main
        import sys
        
        # Get video name and set output directory to video-specific folder
        video_name = os.path.splitext(os.path.basename(input_video))[0]
        video_output_dir = os.path.dirname(csv_path)  # Same folder as CSV
        
        # Set up arguments for analysis pipeline
        original_argv = sys.argv
        sys.argv = ['game_analysis/index.py', '--csv_path', csv_path, '--output_dir', video_output_dir]
        
        # Run analysis
        analysis_main()
        
        # Restore original argv
        sys.argv = original_argv
        
    except ImportError as e:
        print(f"\nError: Could not import game_analysis module: {e}")
        print("Make sure all required packages are installed:")
        print("  pip install scikit-learn matplotlib seaborn")
    except Exception as e:
        print(f"\nError running game analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
    