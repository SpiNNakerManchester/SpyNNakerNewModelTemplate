# main interface to use the spynnaker related tools.
# ALL MODELS MUST INHERIT FROM THIS
from spynnaker.pyNN.models.neuron.abstract_population_vertex \
    import AbstractPopulationVertex

from spynnaker.pyNN.models.neuron.input_types.input_type_current \
    import InputTypeCurrent
from python_models.neuron.neuron_models.my_neuron_model \
    import MyNeuronModel
from spynnaker.pyNN.models.neuron.synapse_types.synapse_type_exponential\
    import SynapseTypeExponential
from python_models.neuron.threshold_types.my_threshold_type \
    import MyThresholdType


class MyModelCurrExpMyThreshold(AbstractPopulationVertex):

    # the maximum number of atoms per core that can be supported
    _model_based_max_atoms_per_core = 256

    # default parameters for this build. Used when end user has not entered any
    default_parameters = {
        'tau_syn_E': 5.0, 'tau_syn_I': 5.0,
        'i_offset': 0, 'my_parameter': -70.0,
        'my_threshold_parameter': 0.5,
        'threshold_value': -10.0}

    def __init__(
            self, n_neurons, spikes_per_second=None, ring_buffer_sigma=None,
            incoming_spike_buffer_size=None, constraints=None, label=None,

            # neuron model parameters
            my_parameter=default_parameters['my_parameter'],
            i_offset=default_parameters['i_offset'],

            # threshold types parameters
            my_threshold_parameter=(
                default_parameters['my_threshold_parameter']),
            threshold_value=default_parameters['threshold_value'],

            # synapse type parameters
            tau_syn_E=default_parameters['tau_syn_E'],
            tau_syn_I=default_parameters['tau_syn_I'],

            # state variables
            v_init=None):

        # create neuron model class
        neuron_model = MyNeuronModel(
            n_neurons, i_offset, my_parameter)

        # create synapse type model
        synapse_type = SynapseTypeExponential(
            n_neurons, tau_syn_E, tau_syn_I)

        # create input type model
        input_type = InputTypeCurrent()

        # create threshold type model
        threshold_type = MyThresholdType(
            n_neurons, threshold_value, my_threshold_parameter)

        # create additional inputs
        additional_input = None

        # instantiate the sPyNNaker system by initialising
        #  the AbstractPopulationVertex
        AbstractPopulationVertex.__init__(

            # standard inputs, do not need to change.
            self, n_neurons=n_neurons, label=label,
            spikes_per_second=spikes_per_second,
            ring_buffer_sigma=ring_buffer_sigma,
            incoming_spike_buffer_size=incoming_spike_buffer_size,

            max_atoms_per_core=(
                MyModelCurrExpMyThreshold._model_based_max_atoms_per_core),

            # the various model types
            neuron_model=neuron_model, input_type=input_type,
            synapse_type=synapse_type, threshold_type=threshold_type,
            additional_input=additional_input,

            # the model a name (shown in reports)
            model_name="MyModelCurrExpMyThreshold",

            # the matching binary name
            binary="my_model_curr_exp_my_threshold.aplx")

    @staticmethod
    def get_max_atoms_per_core():

        return MyModelCurrExpMyThreshold._model_based_max_atoms_per_core

    @staticmethod
    def set_max_atoms_per_core(new_value):

        MyModelCurrExpMyThreshold._model_based_max_atoms_per_core = new_value
