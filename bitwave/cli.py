"""
Command-line interface for Bitwave operations.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .core import BitwaveFile

def main():
    parser = argparse.ArgumentParser(description='Bitwave Audio Format Tools')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get information about a Bitwave file')
    info_parser.add_argument('file', type=str, help='Path to Bitwave file')
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert audio files to Bitwave format')
    convert_parser.add_argument('input', type=str, help='Input audio file')
    convert_parser.add_argument('output', type=str, help='Output Bitwave file')
    convert_parser.add_argument('--bpm', type=float, help='BPM value')
    
    args = parser.parse_args()
    
    if args.command == 'info':
        try:
            bw_file = BitwaveFile(args.file)
            bw_file.read()
            metadata = bw_file.get_metadata()
            print("\nBitwave File Information:")
            print(f"Version: {metadata['version']}")
            print(f"Sample Rate: {metadata['sample_rate']} Hz")
            print(f"Channels: {metadata['channels']}")
            print(f"Duration: {metadata['duration']:.2f} seconds")
            if metadata['bpm']:
                print(f"BPM: {metadata['bpm']}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
            
    elif args.command == 'convert':
        # TODO: Implement conversion from other formats
        print("Conversion not yet implemented", file=sys.stderr)
        sys.exit(1)
        
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main() 