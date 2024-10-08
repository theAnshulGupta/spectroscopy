import gdspy
gdspy.current_library = gdspy.GdsLibrary()

# Chip and frame parameters
chip_height = 13000  # Slightly larger than 0.5"
chip_width = 15500   # Slightly larger than 0.6"
frame_height = chip_height - 2000
frame_width = chip_width - 2000
text_offset = 200
text_height = 400
text_width = 1500
text_frame_width = 100
block_size = 20   # Size of each Tetris block unit (perfect squares)
spacing = block_size/5       # Slightly reduced spacing for a tighter design

# Setup .gds file
lib = gdspy.GdsLibrary()
main_cell = lib.new_cell('Main')

# Draw the frame for design
frame = gdspy.Rectangle((-chip_width / 2, -chip_height / 2), (chip_width / 2, chip_height / 2))
inner = gdspy.Rectangle((-frame_width / 2, -frame_height / 2), (+frame_width / 2, +frame_height / 2))
frame = gdspy.boolean(frame, inner, 'not')

# Add label to frame
text_start = (-frame_width / 2 - text_offset, frame_height / 2 + text_offset)
this_text = "Anshul Gupta"
this_title = gdspy.Text(this_text, text_height, position=(text_start[0] + text_frame_width, text_start[1] + text_frame_width))
bb = this_title.get_bounding_box()
text_frame = gdspy.Rectangle(bb[0] - text_frame_width, bb[1] + text_frame_width)
frame = gdspy.boolean(frame, text_frame, 'not')
main_cell.add(frame)
main_cell.add(this_title)

def square(x, y):
    return gdspy.Rectangle((x, y), (x + 2 * block_size, y + 2 * block_size))

def add_block(block_func, x, y):
    block = block_func(x, y)
    if isinstance(block, list):
        for sub_block in block:
            main_cell.add(sub_block)
    else:
        main_cell.add(block)

x_start = -frame_width / 2 + block_size
y_start = -frame_height / 2 + block_size

row = 0
x = x_start + spacing + block_size*2
y = y_start + 2 * block_size + spacing
extra = block_size + spacing

for i in range(0,186):
    for j in range(0,270):
        add_block(square, x + block_size*2*i+spacing*8*i, y+block_size*2*j)

file_name = "diffraction.gds"
lib.write_gds(file_name)