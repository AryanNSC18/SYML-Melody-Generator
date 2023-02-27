from collections import defaultdict
from pydub.generators import Sine


def note_to_freq(note, epsilon=440.0):

    return (2.0 ** ((note - 69) / 12.0)) * epsilon

def wav_gen(output_file,mid):
    tempo =100
    for track in mid.tracks:
        curr_pos = 0.0

        curr_notes = defaultdict(dict)

        for mel in track:
            tick_ms = (60000.0 / tempo) / mid.ticks_per_beat
            tem = tick_ms * mel.time
            curr_pos += tem

            if mel.type == 'note_on':
                curr_notes[mel.channel][mel.note] = (curr_pos, mel)

            if mel.type == 'note_off':
                start_pos, start_msg = curr_notes[mel.channel].pop(mel.note)

                duration = curr_pos - start_pos

                signal_generator = Sine(note_to_freq(mel.note))
                rendered = signal_generator.to_audio_segment(duration=duration - 50, volume=-20).fade_out(100).fade_in(30)

                output_file = output_file.overlay(rendered, start_pos)

    output_file.export("Generated_mels/SYML_WAV.wav", format="wav") # path to store generated wav