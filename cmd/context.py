class ctx:
    # This is used to have a simple interface for all commands. Otherwise we would have
    # to adjust a lot of files when introducing new parameters ...

    def __init__(self, session, filterExpr, sortExpr, sqlFile, sqlStmt, scriptDir, verbose):
        self.session = session
        self.filterExpr = filterExpr
        self.sortExpr = sortExpr
        self.sqlStmt = sqlStmt
        self.sqlFile = sqlFile
        self.cols = []
        self.scriptDir = scriptDir

        if verbose:
            self.verbose = verbose
        else:
            self.verbose = 0
