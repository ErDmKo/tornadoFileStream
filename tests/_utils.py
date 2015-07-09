import mimetypes
import os


def file_count(directory):
    _, _, filles = next(os.walk(directory))
    return len(filles)


def encode_multipart_formdata(files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be
    uploaded as files.
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = b'----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = b'\r\n'
    L = []
    for (key, filename, value) in files:
        L.append(b'--' + BOUNDARY)
        L.append(
            'Content-Disposition: form-data; name="{0}";'
            ' filename="{1}"'.format(
                key, filename
            ).encode('utf-8')
        )
        L.append('Content-Type: {0}'.format(
            get_content_type(filename)).encode('utf-8')
        )
        L.append(b'')
        L.append(value)
    L.append(b'--' + BOUNDARY + b'--')
    L.append(b'')
    body = CRLF.join(L)
    content_type = b'multipart/form-data; boundary=' + BOUNDARY
    return content_type, body


def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
