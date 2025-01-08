from .sc import sc_write


def write(self, filename, format="sc", **kwargs):
    if format == "sc":
        write_shakecore(self, filename)
    else:
        self.to_obspy().write(filename, format, **kwargs)


def write_shakecore(self, filename):
    sc_write(self, filename)
