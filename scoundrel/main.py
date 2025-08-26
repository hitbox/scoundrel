from .argument_parser import argument_parser

def main(argv=None):
    """
    Command line interface.
    """
    parser = argument_parser()
    args = parser.parse_args(argv)
    func = args.func
    delattr(args, 'func')
    func(args)
