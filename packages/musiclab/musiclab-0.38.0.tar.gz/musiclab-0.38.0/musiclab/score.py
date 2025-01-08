from .fluidmidi.pyside.midi import *

class TrackSetupMeta(FluidNode):
    def __init__(self, name, tempo=None, tsig=None):

        super().__init__([TrackName(name=name)])
        if tempo:
            self.append(TempoSet(bpm=tempo))
        if tsig:
            self.append(TimeSignature(numerator=tsig[0], denominator=tsig[1]))

class SetPitchBendSensitivity(FluidNode):
    def __init__(self, semitones=None, cents=None):
        l = [RPNSelectPitchBendSensitivity()]
        if semitones:
            l.append(ControlDataEntry(msb=semitones))
        if cents:
            l.append(ControlDataEntry(lsb=cents))
        l.append(RPNNullFunction())
        super().__init__(l)

class TrackSetupChannel(FluidNode):
    def __init__(self, vol=80, balance=0.5,
                 poly=True, omni=False,
                 bank_lsb=None, bank_msb=None, program=0,
                 max_bend_semitone=None, max_bend_cents=None):

        super().__init__([
            ControlChannelVolume(pct=float(vol)),
            ControlBalance(abs=balance),
        ])

        if omni:
            self.append(OmniOn())
        else:
            self.append(OmniOff())

        if poly:
            self.append(PolyOn())
        else:
            self.append(MonoOn())

        if bank_msb or bank_lsb:
            self.append(BankProgram(lsb=bank_lsb, msb=bank_msb, program=program))
        else:
            self.append(ProgramChange(program=program))

        if max_bend_semitone or max_bend_cents:
            self.append(SetPitchBendSensitivity(max_bend_semitone, max_bend_cents))

class TimeLine(FluidNode):
    def __init__(self):
        super().__init__([])

    def add_time_signature(self, time, tsig):
        super().append(TimeSignature(time=time, numerator=tsig[0], denominator=tsig[1]))

    def add_tempo_change(self, time, bpm):
        super().append(TempoSet(time=time, bpm=bpm))

    def add_marker(self, time, text):
        super().append(Text(time=time, text=text))
