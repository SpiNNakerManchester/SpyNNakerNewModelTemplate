# main interface to use the spynnaker related tools.
from spynnaker.pyNN.models.neuron.abstract_population_vertex \
    import AbstractPopulationVertex

from spynnaker.pyNN.models.neuron.input_types.input_type_current \
    import InputTypeCurrent
from python_models.neuron.neuron_models.my_neuron_model \
    import MyNeuronModel
from python_models.neuron.synapse_types.my_synapse_type \
    import MySynapseType
from spynnaker.pyNN.models.neuron.threshold_types.threshold_type_static \
    import ThresholdTypeStatic


class MyModelCurrMySynapseType(AbstractPopulationVertex):

    # the maximum number of atoms per core that can be supported
    _model_based_max_atoms_per_core = 256

    # default parameters for this build. Used when end user has not entered any
    default_parameters = {
        'v_thresh': -50.0, 'my_ex_synapse_parameter': 0.1,
        'my_in_synapse_parameter': 0.1,
        'i_offset': 0, 'my_parameter': -70.0}

    def __init__(
            self, n_neurons, machine_time_step, timescale_factor,
            spikes_per_second=None, ring_buffer_sigma=None,
            incoming_spike_buffer_size=None,
            incoming_spike_with_data_buffer_size=None,
            constraints=None, label=None,

            # neuron model parameters
            my_parameter=default_parameters['my_parameter'],
            i_offset=default_parameters['i_offset'],

            # threshold types parameters
            v_thresh=default_parameters['v_thresh'],

            # synapse type parameters
            my_ex_synapse_parameter=default_parameters[
                'my_ex_synapse_parameter'],
            my_in_synapse_parameter=default_parameters[
                'my_in_synapse_parameter'],

            # state variables
            v_init=None):

        # create neuron model class
        neuron_model = MyNeuronModel(
            n_neurons, machine_time_step, i_offset, my_parameter)

        # create synapse type model
        synapse_type = MySynapseType(
            n_neurons, machine_time_step, my_ex_synapse_parameter,
            my_in_synapse_parameter)

        # create input type model
        input_type = InputTypeCurrent()

        # create threshold type model
        threshold_type = ThresholdTypeStatic(n_neurons, v_thresh)

        # create additional inputs
        additional_input = None

        # instantiate the sPyNNaker system by initialising
        #  the AbstractPopulationVertex
        AbstractPopulationVertex.__init__(

            # standard inputs, do not need to change.
            self, n_neurons=n_neurons, label=label,
            machine_time_step=machine_time_step,
            timescale_factor=timescale_factor,
            spikes_per_second=spikes_per_second,
            ring_buffer_sigma=ring_buffer_sigma,
            incoming_spike_buffer_size=incoming_spike_buffer_size,
            incoming_spike_with_data_buffer_size=(
                incoming_spike_with_data_buffer_size),

            max_atoms_per_core=(
                MyModelCurrMySynapseType._model_based_max_atoms_per_core),

            # the various model types
            neuron_model=neuron_model, input_type=input_type,
            synapse_type=synapse_type, threshold_type=threshold_type,
            additional_input=additional_input,

            # the model a name (shown in reports)
            model_name="MyModelMySynapseType",

            # the matching binary name
            binary="my_model_curr_my_synapse_type.aplx")

    @staticmethod
    def set_model_max_atoms_per_core(new_value):

        MyModelCurrMySynapseType._model_based_max_atoms_per_core = new_value
