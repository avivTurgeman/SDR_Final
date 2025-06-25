# Remote Button Decoder
from gnuradio import gr
import pmt

COMMAND_MAP = {
    0x1: "Lock pressed",
    0x2: "Unlock pressed",
}

def bits_to_int(bits):
    val = 0
    for b in bits:
        val = (val<<1) | b
    return val

class remote_button_decoder(gr.basic_block):
    def __init__(self):
        gr.basic_block.__init__(self, name="Button Decoder", in_sig=None, out_sig=None)
        self.message_port_register_in(pmt.intern("in"))
        self.set_msg_handler(pmt.intern("in"), self.handle_pdu)
        self.message_port_register_out(pmt.intern("out"))

    def handle_pdu(self, pdu):
        meta = pmt.car(pdu)
        data = pmt.cdr(pdu)
        try: bits = list(pmt.u8vector_elements(data))
        except: bits = list(pmt.to_python(data))
        if len(bits) < 20: return
        cmd = bits_to_int(bits[16:20])         # הנח שה־command ב-4 הביטים הללו
        text = COMMAND_MAP.get(cmd)
        if text:
            self.message_port_pub(pmt.intern("out"), pmt.cons(meta, pmt.string_to_symbol(text)))
