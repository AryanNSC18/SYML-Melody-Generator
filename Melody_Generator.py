import json
import numpy as np
from tensorflow import keras
import music21 as m21

seq_len = 64
mapping_path = "/SYML_Maps.json" #SYML_Maps path

class LoFiGen:

    def __init__(self,model_path="/Melody_lstm_model.h5"): # path to model file
        self.model_path = model_path
        self.model = keras.models.load_model(model_path)

        with open(mapping_path,"r") as fp:
            self.mappings = json.load(fp)

        self._start_symbols = ["/"]*seq_len
    def gen_lofi(self,seed,num_step,max_seq_len,tem):
        seed = seed.split()
        melody = seed
        seed = self._start_symbols + seed

        seed = [self.mappings[symbol] for symbol in seed]

        for _ in range(num_step):
            seed = seed[-max_seq_len:]
            hot_encode = keras.utils.to_categorical(seed,num_classes=len(self.mappings))
            hot_encode = hot_encode[np.newaxis,...]

        #probab
            probability = self.model.predict(hot_encode)[0]
            output_int = self.sample_with_tem(probability,tem)
            seed.append(output_int)

            output_symb = [k for k,v in self.mappings.items() if v== output_int][0]
            if output_symb == "/":
                break
            melody.append(output_symb)
        return melody


    def sample_with_tem(self,prob,temp):
        prediction = np.log(prob)/temp
        probabilities = np.exp(prediction)/np.sum(np.exp(prediction))

        choices = range(len(probabilities))
        index = np.random.choice(choices,p=probabilities)

        return index
    def save_lofi(self,lofi_tune,step_dur =0.25,format="midi",file_name= r"Generated_mels/SYML_AI_midi.mid"):

        stream = m21.stream.Stream()
        symbol_start = None
        step_count = 0
        for i, symbol in enumerate(lofi_tune):

            if symbol != "_" or i + 1 == len(lofi_tune):

                if symbol_start is not None:

                    quarter_length_duration = step_dur * step_count

                    if symbol_start == "r":
                        m21_event = m21.note.Rest(quarterLength=quarter_length_duration)
                    else:
                        m21_event = m21.note.Note(int(symbol_start), quarterLength=quarter_length_duration)

                    stream.append(m21_event)
                    step_count = 1
                symbol_start = symbol
            else:
                step_count += 1
        stream.write(format, file_name)
