import time
from HyperGP.libs.primitive_set import PrimitiveSet
from HyperGP.mods.tree2graph import ExecutableGen
from HyperGP.operators.execution.tree_exec.compiler_v2 import compile_v2
from HyperGP.operators.execution.tree_exec.compiler_v1 import compile_v1
import numpy as np
from HyperGP.mods.cash_manager import CashManager
from HyperGP import Tensor


class ExecMethod:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError("No find '__call__' implement")

class Executor(ExecMethod):
    def __init__(self):
        self.length_clt = 0
        pass
    """
    input: (n_terms, dataset_size)
    """
    def __call__(self, progs, input:np.array, pset: PrimitiveSet, cashset:CashManager=None):
        # print("prog mean len: ", np.mean([len(prog.list()) for prog in progs]))
        '''pre-conversion'''
        exec_list, states = ExecutableGen()(progs, pset, cashset)

        '''compile and run'''
        if pset.mod and len(input.shape) == 2 and (isinstance(input, Tensor) or isinstance(input, np.ndarray) or isinstance(input, list)):
            expr = compile_v1(exec_list, pset, states)
            # print("here????")
            output, records = expr(input)
            # expr2 = compile_v2(exec_list, pset, states)
            # output2, _ = expr2(input)
            # # print(output)
            # # print(output2)
            # # print(input)
            # print(output[0].numpy()[output[0].numpy() != output2[0].numpy()])
            # print(output2[0].numpy()[output[0].numpy() != output2[0].numpy()])
            # assert (output[0].numpy() == output2[0].numpy()).all()
        else:
            expr = compile_v2(exec_list, pset, states)
            output, records = expr(input)
        return output, records

def executor(progs, input, pset: PrimitiveSet, cashset:CashManager=None):
    """
    Execute the GP programs

    Args:
        progs(list): The GP programs need to be executed.
        input(``HyperGP.Tensor`` or ``numpy.ndarray`` or ``list``): shape = (feature size, ...)
        pset(``HyperGP.PrimitiveSet``): used for the progs

    Returns:
        outputs: The outputs generated by the progs with the given inputs.
        records: The outputs of the record nodes.

    Examples:
        
        >>> from HyperGP import executor, PrimitiveSet, Population
        >>> import numpy as np

        >>> # Generae the primitive set
        >>> pset = PrimitiveSet(
                input_arity=1,
                primitive_set=[
                ('add', HyperGP.add, 2),
                ('sub', HyperGP.sub, 2),
                ('mul', HyperGP.mul, 2),
                ('div', HyperGP.div, 2),
            ])

        >>> # Generate the input data
        >>> input_array = Tensor(np.random.uniform(0, 10, size=(1, 10000)))

        >>> # Initialize the population
        >>> pop = Population()
        >>> pstates = ProgBuildStates(pset=pset, depth_rg=[2, 6], len_limit=100)
        >>> pop.initPop(pop_size=pop_size, prog_paras=pstates)

        >>> # Execute the individuals
        >>> output, _ = executor(pop.states['progs'].indivs, input_array, pset)

    """
    return Executor()(progs, input, pset, cashset)

"""TEST"""
if "__name__" == "__main__":
    pass


