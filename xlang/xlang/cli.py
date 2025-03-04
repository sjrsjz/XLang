#!/usr/bin/env python3
import sys
import os
import argparse
import json
import time
import traceback
from xlang.xlang.lang import XLang


def main():
    """X Lang command line tool entry point"""
    parser = argparse.ArgumentParser(
        description="X Lang - Lightweight programming language"
    )
    parser.add_argument("-c", "--code", help="Execute X Lang code")
    parser.add_argument("-f", "--file", help="Execute X Lang code from file")
    parser.add_argument("-o", "--output", help="Output file for compiled code")
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Start interactive mode"
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="Show version information"
    )
    parser.add_argument(
        "--ast", action="store_true", help="Output abstract syntax tree"
    )
    parser.add_argument(
        "--ir", action="store_true", help="Output intermediate representation"
    )
    parser.add_argument("--time", action="store_true", help="Show execution time")

    args = parser.parse_args()
    xlang = XLang()

    # Show version information
    if args.version:
        print("X Lang version 0.1.0")
        return

    # Handle command line arguments
    if args.code:
        # Direct code execution
        try:
            start_time = time.time()

            if args.ast:
                ast = xlang.parse(args.code)
                print(json.dumps(ast.to_dict(), ensure_ascii=False))
            elif args.ir:
                ir = xlang.compile(args.code)
                print(json.dumps(ir.export_to_dict(), ensure_ascii=False))
            else:
                result = xlang.execute(args.code)
                if result is not None:
                    print(result)

            if args.time:
                print(f"Execution time: {time.time() - start_time:.6f} seconds")
        except Exception as e:
            if args.debug:
                traceback.print_exc()
            else:
                print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.file:
        try:
            # Execute file
            with open(args.file, "r", encoding="utf-8") as f:
                code = f.read()

            start_time = time.time()

            # If output file is specified, compile to .xir
            if args.output:
                ir = xlang.compile(code)
                # Ensure output directory exists
                output_dir = os.path.dirname(os.path.abspath(args.output))
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                # Write compilation result
                with open(args.output, "w", encoding="utf-8") as out_file:
                    out_file.write(
                        json.dumps(ir.export_to_dict(), ensure_ascii=False)
                    )
                print(f"Compiled to: {args.output}")
            elif args.ast:
                ast = xlang.parse(code)
                print(json.dumps(ast.to_dict(), ensure_ascii=False))
            elif args.ir:
                ir = xlang.compile(code)
                print(json.dumps(ir.export_to_dict(), ensure_ascii=False))
            else:
                # Direct execution
                result = xlang.execute(code)
                if result is not None:
                    print(result)

            if args.time:
                print(f"Execution time: {time.time() - start_time:.6f} seconds")
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            if args.debug:
                traceback.print_exc()
            else:
                print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.interactive:
        # Interactive mode
        print("X Lang Interactive Mode")
        print("Enter 'exit()' or press Ctrl+C to exit")
        print()

        # Create separate interpreter instance to maintain state
        interpreter = XLang(debug=args.debug if hasattr(args, "debug") else False)

        while True:
            try:
                # Prompt and get user input
                user_input = input(">>> ")

                # Check for exit command
                if user_input.strip() == "exit()":
                    break

                # Execute code
                start_time = time.time()
                result = interpreter.execute(user_input)

                # Show result
                if result is not None:
                    print(result)

                if args.time:
                    print(f"Execution time: {time.time() - start_time:.6f} seconds")

            except KeyboardInterrupt:
                print("\nExited")
                break
            except Exception as e:
                if args.debug:
                    traceback.print_exc()
                else:
                    print(f"Error: {e}")
    else:
        # If no arguments provided, show help
        parser.print_help()


if __name__ == "__main__":
    main()
