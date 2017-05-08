from spynnaker.pyNN.models.neuron.neuron_models\
    .neuron_model_leaky_integrate_and_fire \
    import NeuronModelLeakyIntegrateAndFire
from python_models.neuron.synapse_types.diff_synapse \
    import DiffSynapseType
from spynnaker.pyNN.models.neuron.input_types.input_type_current \
    import InputTypeCurrent
from spynnaker.pyNN.models.neuron.threshold_types.threshold_type_static \
    import ThresholdTypeStatic
from spynnaker.pyNN.models.neuron.abstract_population_vertex \
    import AbstractPopulationVertex

class IFCurrExpDiff(AbstractPopulationVertex):
    """ Leaky integrate and fire neuron with a combined decaying \
        current inputs: A-B to create humped synaptic input
    """

    _model_based_max_atoms_per_core = 255

    default_parameters = {
        'tau_m': 20.0,
        'cm': 1.0,
        'v_rest': -65.0,
        'v_reset': -65.0,
        'v_thresh': -50.0,
        'exc_A_decay': 6,
        'exc_B_decay': 8,
        'inh_decay': 5.0,
        'tau_refrac': 0.1,
        'i_offset': 0}

    def __init__(
            self, n_neurons, spikes_per_second=None, ring_buffer_sigma=None,
            incoming_spike_buffer_size=None, constraints=None, label=None,
            tau_m=default_parameters['tau_m'], cm=default_parameters['cm'],
            v_rest=default_parameters['v_rest'],
            v_reset=default_parameters['v_reset'],
            v_thresh=default_parameters['v_thresh'],
            exc_A_decay=default_parameters['exc_A_decay'],
            exc_B_decay=default_parameters['exc_B_decay'],
            inh_decay=default_parameters['inh_decay'],
            tau_refrac=default_parameters['tau_refrac'],
            i_offset=default_parameters['i_offset'], v_init=None):

        exc_A_init = 0.0
        exc_B_init = 0.0
        inh_init = 0.0

        # Construct neuron/synapse objects
        neuron_model = NeuronModelLeakyIntegrateAndFire(
            n_neurons, v_init, v_rest, tau_m, cm, i_offset,
            v_reset, tau_refrac)

        synapse_type = DiffSynapseType( n_neurons,
                exc_A_decay,
                exc_A_init,
                exc_B_decay,
                exc_B_init,
                inh_decay,
                inh_init)

        # synapse_type = SynapseTypeExponential(
        #     n_neurons, tau_syn_E, tau_syn_I)

        input_type = InputTypeCurrent()
        threshold_type = ThresholdTypeStatic(n_neurons, v_thresh)

        AbstractPopulationVertex.__init__(
            self, n_neurons=n_neurons, binary="IF_curr_exp_diff.aplx", label=label,
            max_atoms_per_core=IFCurrExpDiff._model_based_max_atoms_per_core,
            spikes_per_second=spikes_per_second,
            ring_buffer_sigma=ring_buffer_sigma,
            incoming_spike_buffer_size=incoming_spike_buffer_size,
            model_name="IF_curr_exp_diff", neuron_model=neuron_model,
            input_type=input_type, synapse_type=synapse_type,
            threshold_type=threshold_type, constraints=constraints)

    @staticmethod
    def set_model_max_atoms_per_core(new_value):
        IFCurrExpDiff._model_based_max_atoms_per_core = new_value

    @staticmethod
    def get_max_atoms_per_core():
        return IFCurrExpDiff._model_based_max_atoms_per_core
