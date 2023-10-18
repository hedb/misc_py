import uuid

base_command = '''
  {
  "id": "__UUID__",
  "comment": "",
  "command": "runScript",
  "target": "window.scrollTo(0,__scroll_pixel__)",
  "targets": [],
  "value": ""
},
'''

total_script = ''

scroll_pixels = 100
for i in range(0,100):
    total_script += base_command.replace('__UUID__',str(uuid.uuid4())).replace('__scroll_pixel__',str(scroll_pixels))
    scroll_pixels += 500
print(total_script)