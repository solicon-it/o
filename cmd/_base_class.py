import o.cmd.context as context


class OraCommand:
    def __init__(self, ctx):
        self.ctx = ctx
        self.cols = []

    def checkColNames(self, filterArgs):
        "only simple filter expressions [colname value] are checks here. (So no filter provided via flag '-f2'!"
        if filterArgs:
            simple_filter = list(filter(lambda f: len(f) == 2, filterArgs))
            if simple_filter:
                cols = list(list(zip(*simple_filter))[0])
                for c in cols:
                    if c.upper() not in self.cols:
                        print("Column '{}' is not allowed here!\n(Only {} are possible.)".format(
                            c.upper(), self.cols))
                        exit(1)

    # The default is to do an upper() for all values provided via -f flag.
    # But in some situations (e.g. "parameters") we must not do an upper() for some
    # columns, because the query would not find any matches doing so.
    def adjustCase_forColumnValues(self, filterArgs, noAdjustCols):
        if filterArgs:
            for f in filterArgs:
                if len(f) > 1:
                    if f[0].upper() not in noAdjustCols:
                        f[1] = f[1].upper()
        return filterArgs

    def predicateExpr(self, filterArgs):
        pred = ""
        if filterArgs:
            for f in filterArgs:
                if len(f) == 1:
                    # situation: We apply one predicate via -f2 flag.
                    pred += "and {} ".format(f[0])
                else:
                    pred += "and {} like '{}' ".format(f[0], f[1])
        return pred

    def sortExpr(self, sortArgs):
        sort = ""
        if sortArgs != None:
            i = 0
            for f in sortArgs:
                if len(f) == 1:
                    f = [f[0], "asc"]

                if i == 0:
                    sort += "{} {}".format(f[0], f[1])
                else:
                    sort += ", {} {}".format(f[0], f[1])
                i += 1
        else:
            sort = "1"

        return sort

    def printSQL(self, SQL):
        if self.ctx.verbose >= 2:
            print("Predicates = {}".format(self.ctx.filterExpr))
            print(SQL)

    def execute(self, predicates, sort_order):
        pass


