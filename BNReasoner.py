from typing import Union
from BayesNet import BayesNet


class BNReasoner:
    def __init__(self, net: Union[str, BayesNet]):
        """
        :param net: either file path of the bayesian network in BIFXML format or BayesNet object
        """
        if type(net) == str:
            # constructs a BN object
            self.bn = BayesNet()
            # Loads the BN from an BIFXML file
            self.bn.load_from_bifxml(net)
        else:
            self.bn = net

    # TODO: This is where your methods should go

    def multi_factor(self, lista):

        while len(lista) > 1:
            x = lista[0]
            y = lista[1]
            new = []
            overlapping_labels = x.columns[:-1].intersection(y.columns[:-1])
            overlapping_labels = overlapping_labels.tolist()
            if x.columns[-1] != "p":
                x.rename(columns={x.columns[-1]: 'p'}, inplace=True)
            if y.columns[-1] != "p":
                y.rename(columns={y.columns[-1]: 'p'}, inplace=True)
            z = x.merge(y, on=overlapping_labels, how="outer")
            z["factor"] = z['p_x'] * z['p_y']
            z = z.drop(['p_x', 'p_y'], axis=1)
            lista.pop(0)
            lista.pop(0)
            lista.append(z)
        return z

        #if len(self.bn.get_cpt(variable_1)) > len(self.bn.get_cpt(variable_2)):
        #    x = self.bn.get_cpt(variable_2)
        #    y = self.bn.get_cpt(variable_1)
        #else:
        #    x = self.bn.get_cpt(variable_1)
        #    y = self.bn.get_cpt(variable_2)
        #new = y.drop("p", axis = 1)
        #f = []
        #for index, row in x.iterrows():
        #    for inex, rw in y.iterrows():
        #        if row[variable_1] == rw[variable_1]:
        #            factor = row['p'] * rw["p"]
        #            f.append(factor)
        #new["factor"] = f
        #print(new)



    def summing_out(self, cpt, variable):
        df = cpt.drop(variable, axis = 1)
        d = df.columns[-1]
        agg = {d: 'sum'}
        groups = df.columns.to_list()[:-1]
        df_new = df.groupby(groups, as_index=False).aggregate(agg).reindex(columns=df.columns)
        return df_new

    def maxing_out(self, cpt, variable):
        #df = cpt.drop(variable, axis = 1)
        #d = df.columns[-1]
        #agg = {d: 'max'}
        #groups = df.columns.to_list()[:-1]
        #df_new = cpt.groupby(groups, as_index=False).aggregate(agg).reindex(columns=cpt.columns)

        df_other = cpt.loc[cpt.groupby('Sprinkler?')[cpt.columns[-1]].idxmax()].reset_index(drop=True)
        df_other["instantiation"] = f"{variable} =" + df_other[variable].astype(str)
        df_other = df_other.drop(variable, axis =1 )
        return df_other

    def prior_marginals(self, order):
        all = self.bn.get_all_cpts()
        x = list(all.values())
        for variable in order:
            mention = []
            for cpt in x:
                if variable in cpt.columns.tolist():
                    mention.append(cpt)
            factor = self.summing_out(self.multi_factor(mention),variable)
            y = []
            for cpt in x:
                if variable not in cpt.columns.tolist():
                    y.append(cpt)
            y.append(factor)
            x = y
        return x





    def get_variables_from_order(self, variable):
        x = self.bn.get_children(variable)
        x.append(variable)
        return x