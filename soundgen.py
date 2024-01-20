"""
A small library for generating and modifying waveforms.
"""
import numpy as np
import scipy.io.wavfile
import time

DEFAULT_SAMPLE_RATE = 48000
DEFAULT_LENGTH = 5
DEFAULT_FREQUENCY = 440
TWO_PI = 2 * np.pi
DEFAULT_AMPLITUDE = 0.2

def _sample_count_array(length: float=DEFAULT_LENGTH,
                        sample_rate: int=DEFAULT_SAMPLE_RATE,
                        extra_samples: int=0) -> np.ndarray:
    return np.arange(sample_rate * length + extra_samples)

def _adjust_range(input_values,
                  original_range = (0,1),
                  new_range = (-1, 1)):
    stretch_factor = (new_range[1] - new_range[0]) / (original_range[1] - original_range[0])
    offset = original_range[0] - new_range[0]
    return input_values * stretch_factor - offset

def _overshoot_for_phase_shift(frequency: float,
                               sample_rate: int,
                               phase: float):
    """
    Find extra number of samples needed to make phase shifting work
    """
    return round(phase * sample_rate / frequency)

def _shift_phase(wave: np.ndarray, extra_samples: int) -> np.ndarray:
    return wave[extra_samples:]

def sine_wave(frequency: float=DEFAULT_FREQUENCY,
              amplitude: float=DEFAULT_AMPLITUDE,
              length: float=DEFAULT_LENGTH,
              sample_rate: int=DEFAULT_SAMPLE_RATE,
              phase: float=0) -> np.ndarray:
    """
    Generates an array of a sinuoidal wave.

    Args:
        frequency (float, optional): Frequency of the wave in hertz. Defaults to `DEFAULT_FREQUENCY`.
        amplitude (float, optional): Amplitude of the wave. This is a dimensionless quantity in range [0,1]. Defaults to `DEFAULT_AMPLITUDE`.
        phase (float, optional): Phase of the wave in turns (1 turn = 360 degrees = 2pi radians). Takes inputs in [0,1). Defaults to 0.
        length (float, optional): Length of the wave in seconds. Defaults to `DEFAULT_LENGTH`.
        sample_rate (int, optional): Number of samples per second. Defaults to `DEFAULT_SAMPLE_RATE`.

    Returns:
        np.ndarray: a sinusoidal wave
    """
    extra_samples = _overshoot_for_phase_shift(frequency, sample_rate, phase)
    sine_array = np.sin(_sample_count_array(length, sample_rate, extra_samples) * frequency * TWO_PI / sample_rate) * amplitude
    sine_array = _shift_phase(sine_array, extra_samples)
    return sine_array.astype(np.float32)

def _sawtooth_basic(frequency: float=DEFAULT_FREQUENCY,
                    length: float=DEFAULT_LENGTH,
                    sample_rate: int=DEFAULT_SAMPLE_RATE,
                    extra_samples: int=0):
    """
    Helper function for sawtooth, pulse, and triangle.
    Generates sawtooth with range [0,1).
    """
    sawtooth_array = _sample_count_array(length, sample_rate, extra_samples) * frequency / DEFAULT_SAMPLE_RATE
    sawtooth_array = sawtooth_array - np.floor_divide(sawtooth_array, 1)
    return sawtooth_array

def _pulse_basic(frequency: float,
        length: float=DEFAULT_LENGTH,
        sample_rate: int=DEFAULT_SAMPLE_RATE,
        duty_cycle: float=0.5,
        extra_samples: int=0):
    """
    Helper function for pulse. May also be useful for pulse LFOs.
    """
    clipper = np.vectorize(lambda x: 0 if x >= duty_cycle else 1)
    pulse_array = _sawtooth_basic(frequency, sample_rate, length, extra_samples)
    pulse_array = clipper(pulse_array)
    return pulse_array

def pulse_wave(frequency: float=DEFAULT_FREQUENCY,
               amplitude: float=DEFAULT_AMPLITUDE,
               length: float=DEFAULT_LENGTH,
               sample_rate: int=DEFAULT_SAMPLE_RATE,
               phase: float=0,
               duty_cycle: float=0.5) -> np.ndarray:
    """
    Generates an array of a pulse wave with a given duty cycle.

    Args:
        frequency (float, optional): Frequency of the wave in hertz. Defaults to `DEFAULT_FREQUENCY`.
        amplitude (float, optional): Amplitude of the wave. This is a dimensionless quantity in range [0,1]. Defaults to `DEFAULT_AMPLITUDE`.
        phase (float, optional): Phase of the wave in turns (1 turn = 360 degrees = 2pi radians). Takes inputs in [0,1). Defaults to 0.
        length (float, optional): Length of the wave in seconds. Defaults to `DEFAULT_LENGTH`.
        sample_rate (int, optional): Number of samples per second. Defaults to `DEFAULT_SAMPLE_RATE`.
        duty_cycle (float, optional): Proportion of time the wave spends in its high position. Takes inputs in [0,1]. 

    Returns:
        np.ndarray: a pulse wave
    """
    extra_samples = _overshoot_for_phase_shift(frequency, sample_rate, phase)
    pulse_array = _pulse_basic(frequency, length, sample_rate, duty_cycle,extra_samples)
    pulse_array = _adjust_range(pulse_array, new_range=(-amplitude, amplitude))
    pulse_array = _shift_phase(pulse_array, extra_samples)
    return pulse_array.astype(np.float32)

def sawtooth_wave(frequency: float=DEFAULT_FREQUENCY,
                  amplitude: float=DEFAULT_AMPLITUDE,
                  length: float=DEFAULT_LENGTH,
                  sample_rate: int=DEFAULT_SAMPLE_RATE,
                  phase: float=0) -> np.ndarray:
    """Generates an array of a sawtooth wave.

    Args:
        frequency (float, optional): Frequency of the wave in hertz. Defaults to `DEFAULT_FREQUENCY`.
        amplitude (float, optional): Amplitude of the wave. This is a dimensionless quantity in range [0,1]. Defaults to `DEFAULT_AMPLITUDE`.
        phase (float, optional): Phase of the wave in turns (1 turn = 360 degrees = 2pi radians). Takes inputs in [0,1). Defaults to 0.
        length (float, optional): Length of the wave in seconds. Defaults to `DEFAULT_LENGTH`.
        sample_rate (float, optional): Number of samples per second. Defaults to `DEFAULT_SAMPLE_RATE`.

    Returns:
        np.ndarray: a sawtooth wave
    """
    # to ensure all wave shapes have the same phase
    phase = (phase + 0.5) % 1
    extra_samples = _overshoot_for_phase_shift(frequency, sample_rate, phase)
    sawtooth_array = _sawtooth_basic(frequency, sample_rate, length, extra_samples)
    sawtooth_array = _adjust_range(sawtooth_array, new_range=(-amplitude, amplitude))
    sawtooth_array = _shift_phase(sawtooth_array, extra_samples)
    return sawtooth_array.astype(np.float32)

def triangle_wave(frequency: float=DEFAULT_FREQUENCY,
                  amplitude: float=DEFAULT_AMPLITUDE,
                  length: float=DEFAULT_LENGTH,
                  sample_rate: int=DEFAULT_SAMPLE_RATE,
                  phase: float=0) -> np.ndarray:
    """Generates an array of a triangle wave.

    Args:
        frequency (float, optional): Frequency of the wave in hertz. Defaults to `DEFAULT_FREQUENCY`.
        amplitude (float, optional): Amplitude of the wave. This is a dimensionless quantity in range [0,1]. Defaults to `DEFAULT_AMPLITUDE`.
        phase (float, optional): Phase of the wave in turns (1 turn = 360 degrees = 2pi radians). Takes inputs in [0,1). Defaults to 0.
        length (float, optional): Length of the wave in seconds. Defaults to `DEFAULT_LENGTH`.
        sample_rate (float, optional): Number of samples per second. Defaults to `DEFAULT_SAMPLE_RATE`.

    Returns:
        np.ndarray: a triangle wave
    """
    # to ensure all wave shapes have the same phase
    phase = (phase + 0.25) % 1
    # no need to do more phase shifting, sawtooth_wave already does it
    triangle_array = np.abs(sawtooth_wave(frequency, amplitude, length, sample_rate, phase))
    triangle_array = _adjust_range(triangle_array,
                                    (0, amplitude),
                                    (-amplitude, amplitude))
    return triangle_array.astype(np.float32)

def white_noise(amplitude: float=DEFAULT_AMPLITUDE,
                length: float=DEFAULT_LENGTH,
                sample_rate: int=DEFAULT_SAMPLE_RATE):
    """Generates an array of white noise.

    Args:
        amplitude (float, optional): Amplitude of the wave. This is a dimensionless quantity in range [0,1]. Defaults to `DEFAULT_AMPLITUDE`.
        length (_type_, optional): Length of the wave in seconds. Defaults to `DEFAULT_LENGTH`.
        sample_rate (_type_, optional): Number of samples per second. Defaults to `DEFAULT_SAMPLE_RATE`.

    Returns:
        np.ndarray: white noise
    """
    rng = np.random.default_rng()
    noise_array = _adjust_range(rng.random(sample_rate * length), new_range=(-amplitude, amplitude))
    return noise_array.astype(np.float32)

def _frequency_sweep_array(f0: float, f1: float,
                          length: float=DEFAULT_LENGTH,
                          sample_rate: int=DEFAULT_SAMPLE_RATE) -> np.ndarray:
    """Helper function for `sine_sweep`"""
    t = _sample_count_array(length, sample_rate)
    total_time = t.shape[0]
    c = (f1 - f0) / total_time
    return c * t * t / 2 + f0 * t

def sine_sweep(f0: float, f1: float,
              amplitude: float=DEFAULT_AMPLITUDE,
              length: float=DEFAULT_LENGTH,
              sample_rate: int=DEFAULT_SAMPLE_RATE) -> np.ndarray:
    """
    Generates an array of a sine wave sweep from a starting frequency `f0` to an ending frequency `f1`.
    
    There is no buffer period for either end of the sweep. There is no guarantee that the waves you attach to either end of this sweep will match phase. If you don't account for this, you may get a nasty clicking sound in your output. Consider using `find_nearest_zero_crossing` to alleviate this.

    Args:
        f0 (float): Starting frequency of the sweep in hertz.
        f1 (float): Ending frequency of the sweep in hertz.
        amplitude (float, optional): Amplitude of the wave. This is a dimensionless quantity in range [0,1]. Defaults to `DEFAULT_AMPLITUDE`.
        length (float, optional): Length of the wave in seconds. Defaults to `DEFAULT_LENGTH`.
        sample_rate (int, optional): Number of samples per second. Defaults to `DEFAULT_SAMPLE_RATE`.

    Returns:
        np.ndarray: a sine wave sweep
    """
    phi = _frequency_sweep_array(f0, f1, length, sample_rate)
    sine_array = np.sin(phi * TWO_PI / sample_rate) * amplitude
    return sine_array.astype(np.float32)

def wave_interpolation(a: np.ndarray, b: np.ndarray,
                       t: float | np.ndarray) -> np.ndarray:
    """
    Creates a linear interpolation between the values of two waveforms.
    
    Args:
        a (np.ndarray): A wave array.
        b (np.ndarray): A wave array of the same length as b. This function is most useful when a and b also have the same frequency and phase.
        t (float or np.ndarray): When `t = 0`, this function returns `a`. When `t = 1`, this function returns `b`.
        
    Returns:
        np.ndarray: a linear interpolation between `a` and `b`
    """
    return ((1-t) * a) + (t * b)

def adsr(attack: float, decay: float,
         sustain: float, release: float, press_time: float,
         sample_rate: int=DEFAULT_SAMPLE_RATE):
    """Produces an ADSR envelope.

    Args:
        attack (float): Attack time in seconds.
        decay (float): Decay time in seconds.
        sustain (float): Sustain level—a dimensionless quantity in [0,1].
        release (float): Release time in seconds.
        press_time (float): Time a fake key is pressed in seconds. If `press_time` is shorter than `attack_time`, this function plays the attack and release in full. If `press_time` cuts off the decay, the decay slope switches midstream to the release slope.
        sample_rate (int, optional): Number of samples per second. Defaults to `DEFAULT_SAMPLE_RATE`.

    Returns:
        np.ndarray: ADSR envelope
    """

    short_press = attack > press_time
    sustain = 1 if short_press else sustain
    
    # deals with press time cutting off decay
    short_decay = max(0, min(decay, press_time - attack))
    decay_ratio = short_decay / decay
    sustain = (1 - decay_ratio) + (decay_ratio * sustain)
    decay = short_decay
    
    remaining_time = max(0, press_time - attack - decay)
    release = release - decay if decay_ratio < 1 else release

    attack_samples = round(attack * sample_rate)
    decay_samples = round(decay * sample_rate)
    sustain_samples = round(remaining_time * sample_rate)
    release_samples = round(release * sample_rate)
    
    a = np.linspace(0, 1, attack_samples)
    d = np.linspace(1, sustain, decay_samples)
    s = np.full(sustain_samples, sustain)
    r = np.linspace(sustain, 0, release_samples)
    
    return np.concatenate((a, d, s, r))
    
def find_nearest_zero_crossing(array: np.ndarray,
                               i: int,
                               positive_slope: bool | None = None) -> int:
    """
    Finds the index of the closest zero crossing to a given index.
    
    If a zero crossing is between samples, this function returns the index closer to `i`. If two zero crossings are equally close, this function returns the crossing with the smaller index, similar to `np.argmin`.

    Args:
        array (np.ndarray): input array
        i (int): given index of array
        positive_slope (bool | None, optional): If this is `None`, this function finds the closest zero crossing regardless of slope. If it's `True`, this function returns the nearest zero crossing with a positive slope. If it's `False`, this function returns the nearest zero crossing with a negative slope. Defaults to `None`.

    Raises:
        ValueError: if positive_slope isn't `True`, `False`, or `None`

    Returns:
        int: index of closest zero crossing.
    """
    signs = np.sign(array)
    differences = np.diff(signs)
    if positive_slope is None:
        crossings = np.where(np.abs(differences) > 0)
    elif positive_slope:
        crossings = np.where(differences > 0)
    elif not positive_slope:
        crossings = np.where(differences < 0)
    else:
        raise ValueError("positive_slope must be boolean or None")
    crossings = crossings[0]
    
    # where there's an actual zero, the previous if/else branches still bring in an adjacent index. this removes these unnecessary extra indices
    sampled_zero_indices = crossings[np.abs(differences[crossings]) == 1]
    bad_indices = sampled_zero_indices[np.where(array[sampled_zero_indices] != 0)[0]]
    crossings = np.setdiff1d(crossings, bad_indices)
    
    crossing_distance = np.abs(crossings-i)
    result_index = crossing_distance.argmin()
    
    result = crossings[result_index]
    return result

def write_wave_to_disk(shape_array,
                       output_name,
                       sample_rate=DEFAULT_SAMPLE_RATE):
    """Writes a given waveform to disk"""
    scipy.io.wavfile.write("{}.wav".format(output_name), sample_rate, shape_array)

def write_and_report_runtime(shape_array,
                             output_name,
                             sample_rate=DEFAULT_SAMPLE_RATE,
                             shape_description="Waveform"):
    """Writes a given waveform to disk and reports its runtime to terminal"""
    start = time.time()
    write_wave_to_disk(shape_array, output_name, sample_rate)
    runtime_ms = round((time.time() - start) * 1000, 3)
    print("{} written in {} ms.".format(shape_description, runtime_ms))
    
if __name__ == '__main__':
    print(triangle_wave().shape)