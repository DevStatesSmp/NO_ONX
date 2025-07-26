from sandbox import sandbox_runner, profile_loader

def main(args):
    profile = profile_loader.load(args.profile)
    result = sandbox_runner.execute(
        target_file=args.file,
        config=profile
    )

    if args.output:
        from src.utils import filelog
        filelog.write_json(args.output, result)
    else:
        print(result["stdout"])