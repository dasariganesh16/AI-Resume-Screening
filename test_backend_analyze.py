import http.client
import uuid

print('health check')
conn = http.client.HTTPConnection('127.0.0.1', 8001)
conn.request('GET', '/api/v1/health/')
res = conn.getresponse()
print(res.status)
print(res.read().decode('utf-8'))

print('analyze test')
boundary = '----WebKitFormBoundary' + uuid.uuid4().hex
lines = []
lines.append('--' + boundary)
lines.append('Content-Disposition: form-data; name="job_description"')
lines.append('')
lines.append('Looking for a Python developer role with backend and AI experience.')
lines.append('--' + boundary)
lines.append('Content-Disposition: form-data; name="resume"; filename="resume.pdf"')
lines.append('Content-Type: application/pdf')
lines.append('')
pdf_data = b'%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Count 1 /Kids [3 0 R] >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT /F1 24 Tf 50 150 Td (Hello World) Tj ET\nendstream\nendobj\n5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000115 00000 n \n0000000224 00000 n \n0000000292 00000 n \ntrailer\n<< /Root 1 0 R /Size 6 >>\nstartxref\n360\n%%EOF\n'
body = b'\r\n'.join([line.encode('latin-1') if isinstance(line, str) else line for line in lines + [pdf_data, '--' + boundary + '--', '']])
conn = http.client.HTTPConnection('127.0.0.1', 8001)
conn.request('POST', '/api/v1/analyze/', body, {'Content-Type': 'multipart/form-data; boundary=' + boundary})
res = conn.getresponse()
print(res.status)
print(res.read().decode('utf-8', 'replace'))
