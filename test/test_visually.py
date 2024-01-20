"""Visual inspection tests. Open the resulting WAV files in Audacity or some other DAW."""
from context import soundgen
from soundgen import *

TEST_SAMPLE_RATE = 44100
TEST_LENGTH = 1
TEST_AMPLITUDE = 0.2

# Inspect the following waveforms to ensure they push the sine wave back as
# desired.

for i in range(10):
    phi = i/10
    write_and_report_runtime(sine_wave(phase=phi, length=TEST_LENGTH), "spt_sine_440_p{}_1s".format(i), shape_description="Sine wave at 440 Hz, {} turns ahead".format(phi))

# Inspect the following waveforms to ensure they all have the same phase. The
# sine, triangle, sawtooth, and 50% pulse waves should have the same zero
# crossings and be positive and negative at the same time. The other pulse
# waves should only start being positive when all the other waves start being
# positive; the crossing point down to negative values shouldn't match.

write_and_report_runtime(sine_wave(length=TEST_LENGTH), "p0_sine_440_1s", shape_description="Sine wave at 440 Hz")
write_and_report_runtime(triangle_wave(length=TEST_LENGTH), "p0_tri_440_1s", shape_description="Triangle wave at 440 Hz")
write_and_report_runtime(sawtooth_wave(length=TEST_LENGTH), "p0_saw_440_1s", shape_description="Sawtooth wave at 440 Hz")
write_and_report_runtime(pulse_wave(length=TEST_LENGTH, duty_cycle=0.125), "p0_pulse125_440_1s", shape_description=r"Pulse wave at 440 Hz (12.5% duty cycle)")
write_and_report_runtime(pulse_wave(length=TEST_LENGTH), "p0_pulse50_440_1s", shape_description=r"Pulse wave at 440 Hz (50% duty cycle)")
write_and_report_runtime(pulse_wave(length=TEST_LENGTH, duty_cycle=0.25), "p0_pulse25_440_1s", shape_description=r"Pulse wave at 440 Hz (25% duty cycle)")
write_and_report_runtime(pulse_wave(length=TEST_LENGTH, duty_cycle=0.75), "p0_pulse75_440_1s", shape_description=r"Pulse wave at 440 Hz (75% duty cycle)")

# These waveforms have a phase of 0.4 turns (144 degreees, pi/5 radians).

write_and_report_runtime(sine_wave(length=TEST_LENGTH, phase=0.4), "p4_sine_440_1s", shape_description="Sine wave at 440 Hz, 0.4 turns ahead")
write_and_report_runtime(triangle_wave(length=TEST_LENGTH, phase=0.4), "p4_tri_440_1s", shape_description="Triangle wave at 440 Hz, 0.4 turns ahead")
write_and_report_runtime(sawtooth_wave(length=TEST_LENGTH, phase=0.4), "p4_saw_440_1s", shape_description="Sawtooth wave at 440 Hz, 0.4 turns ahead")
write_and_report_runtime(pulse_wave(length=TEST_LENGTH, phase=0.4, duty_cycle=0.125), "p4_pulse125_440_1s", shape_description=r"Pulse wave at 440 Hz (12.5% duty cycle), 0.4 turns ahead")
write_and_report_runtime(pulse_wave(length=TEST_LENGTH, phase=0.4), "p4_pulse50_440_1s", shape_description=r"Pulse wave at 440 Hz (50% duty cycle), 0.4 turns ahead")
write_and_report_runtime(pulse_wave(length=TEST_LENGTH, phase=0.4, duty_cycle=0.25), "p4_pulse25_440_1s", shape_description=r"Pulse wave at 440 Hz (25% duty cycle), 0.4 turns ahead")
write_and_report_runtime(pulse_wave(length=TEST_LENGTH, phase=0.4, duty_cycle=0.75), "p4_pulse75_440_1s", shape_description=r"Pulse wave at 440 Hz (75% duty cycle), 0.4 turns ahead")

# This series of waves exists to check is phase shifting works as intended for
# non-decimal frequencies.

write_and_report_runtime(sine_wave(111.1, length=TEST_LENGTH, phase=0.4), "p4n_sine_111-1_1s", shape_description="Sine wave at 111.1 Hz, 0.4 turns ahead")
write_and_report_runtime(triangle_wave(111.1, length=TEST_LENGTH, phase=0.4), "p4n_tri_111-1_1s", shape_description="Triangle wave at 111.1 Hz, 0.4 turns ahead")
write_and_report_runtime(sawtooth_wave(111.1, length=TEST_LENGTH, phase=0.4), "p4n_saw_111-1_1s", shape_description="Sawtooth wave at 111.1 Hz, 0.4 turns ahead")
write_and_report_runtime(pulse_wave(111.1, length=TEST_LENGTH, phase=0.4, duty_cycle=0.125), "p4n_pulse125_111-1_1s", shape_description=r"Pulse wave at 111.1 Hz (12.5% duty cycle), 0.4 turns ahead")
write_and_report_runtime(pulse_wave(111.1, length=TEST_LENGTH, phase=0.4), "p4n_pulse50_111-1_1s", shape_description=r"Pulse wave at 111.1 Hz (50% duty cycle), 0.4 turns ahead")
write_and_report_runtime(pulse_wave(111.1, length=TEST_LENGTH, phase=0.4, duty_cycle=0.25), "p4n_pulse25_111-1_1s", shape_description=r"Pulse wave at 111.1 Hz (25% duty cycle), 0.4 turns ahead")
write_and_report_runtime(pulse_wave(111.1, length=TEST_LENGTH, phase=0.4, duty_cycle=0.75), "p4n_pulse75_111-1_1s", shape_description=r"Pulse wave at 111.1 Hz (75% duty cycle), 0.4 turns ahead")