from tkinter import *
from tkinter import filedialog
import base64
import png

end_of_message = "010110100101011100110101011010110101100000110010001110010110110101011000001100100011000101101100011000110011001101001110011010000101101000110010010101010011110100001010"

window = Tk()
window1 = Tk()
#window1.state("iconic")
window2 = Tk()
#window2.state("iconic")

def get_pixels_from_image(fname):
	img = png.Reader(fname).read()
	pixels = img[2]
	return pixels

def decode_message_from_bytestring(bytestring) :
	bytestring = bytestring.split(end_of_message)[0]
	message = int(bytestring, 2).to_bytes(len(bytestring) // 8, byteorder = "big")
	message = base64.decodebytes(message).decode("utf8", errors = "ignore")
	return message

def decode_pixels(pixels):
	bytestring = [ ]
	for row in pixels:
		for c in row:
			bytestring.append(str(c % 2))
	bytestring = "".join(bytestring)
	message = decode_message_from_bytestring(bytestring)
	return message

def decode(e = None) :
	global window2, path2
	pixels = get_pixels_from_image(path2)
	original_message = decode_pixels(pixels)
	label9 = Label(window2, text = str(original_message), bg = "#9068C7", font = ("Arial Black", 20)).pack(pady = 40)

def select_file_for_decoding() :
	global window2, path2, fileAddress2
	window2.filename = filedialog.askopenfilename(initialdir = "Downloads", title = "Select a PNG file", filetypes = (("png Files", "*.png"), ("All Files", "*.*")))
	label8 = Label(window2, text = window2.filename).place(x = 50, y = 170)
	path2 = window2.filename
	fileAddress2.destroy()

def file_details_for_decoding() :
	global window, window1, window2, window_width, window_height, x, y, path2, fileAddress2
	window.state("iconic")
	window1.state("iconic")
	window2.state("normal")
	window2.title("Image Steganography")
	window2.geometry(f"{window_width}x{window_height}+{x}+{y}")
	label6 = Label(window2, text = "File", fg = "white", bg = "#9068C7", font = ("Times", 14, "bold")).place(x = 10, y = 165)
	fileAddress2 = Entry(window2, width = 80)
	fileAddress2.place(x = 50, y = 170)
	label7 = Label(window2, text = 'Please select a "-enc.png" extension file', fg = "yellow", bg = "#9068C7", font = ("Arial Black", 10)).pack(pady = 100)
	butselect = Button(window2, text = "Select", borderwidth = 5, font = ("Times", 10), command = select_file_for_decoding).place(x = 540, y = 165)
	butclose2 = Button(window2, text = "Close", font = ("Times", 15), borderwidth = 10, command = close).place(x = 265, y = 490)
	butdone2 = Button(window2, text = "OK", font = ("Times", 15), borderwidth = 10, command = decode).place(x = 120, y = 490)
	butback2 = Button(window2, text = "Back", font = ("Times", 15), borderwidth = 10, command = main).place(x = 420, y = 490)
	window2.mainloop()

def write_pixels_to_image(pixels, fname):
	png.from_array(pixels, "RGB").save(fname)

def encode_pixels_with_message(pixels, bytestring):
	"""modifies pixels to encode the contents from bytestring"""
 
	enc_pixels = []
	string_i = 0
	for row in pixels:
		enc_row = []
		for i, char in enumerate(row):
			if string_i >= len(bytestring):
				pixel = row[i]
			else:
				if row[i] % 2 != int(bytestring[string_i]):
					if row[i] == 0:
						pixel = 1
					else:
						pixel = row[i] - 1
				else:
					pixel = row[i]
			enc_row.append(pixel)
			string_i += 1
 
		enc_pixels.append(enc_row)
	return enc_pixels

def encode_message_as_bytestring(message):
	b64 = message.encode("utf8")
	bytes_ = base64.encodebytes(b64)
	bytestring = "".join(["{:08b}".format(x) for x in bytes_])
	bytestring = bytestring
	bytestring += end_of_message
	return bytestring

def encode(e = None) :
	global window1, msg, path1
	label5 = Label(window1, text = "DONE", bg = "#9068C7", font = ("Arial Black", 25)).place(x = 250, y = 400)
	message = msg.get()
	pixels = get_pixels_from_image(path1)
	bytestring = encode_message_as_bytestring(message)
	epixels = encode_pixels_with_message(pixels, bytestring)
	write_pixels_to_image(epixels, path1 + "-enc.png")

def select_file_for_encoding() :
	global window1, path1, fileAddress1
	window1.filename = filedialog.askopenfilename(initialdir = "Downloads", title = "Select a PNG file", filetypes = (("png Files", "*.png"), ("All Files", "*.*")))
	label4 = Label(window1, text = window1.filename).place(x = 50, y = 170)
	path1 = window1.filename
	fileAddress1.destroy()

def file_details_for_encoding() :
	global window, window1, window2, window_width, window_height, x, y, msg, path1, fileAddress1
	window.state("iconic")
	window1.state("normal")
	window2.state("iconic")
	window1.title("Image Steganography")
	window1.geometry(f"{window_width}x{window_height}+{x}+{y}")
	label1 = Label(window1, text = "File", bg = "#9068C7",fg = "white", font = ("Times", 14, "bold")).place(x = 10, y = 165)
	fileAddress1 = Entry(window1, width = 80)
	fileAddress1.place(x = 50, y = 170)
	label2 = Label(window1, text = 'Please SELECT a .png file using the "Select" button', fg = "yellow", bg = "#9068C7", font = ("Arial Black", 10)).pack(pady = 100)
	butselect = Button(window1, text = "Select", borderwidth = 5, font = ("Times", 10), command = select_file_for_encoding).place(x = 540, y = 165)
	label3 = Label(window1, text = "Message", bg = "#9068C7",fg = "white", font = ("Times", 13, "bold")).place(x = 9, y = 326)
	msg = Entry(window1, width = 75)
	msg.place(x = 80, y = 330)
	butclose1 = Button(window1, text = "Close", font = ("Times", 15), borderwidth = 10, command = close).place(x = 265, y = 490)
	butdone1 = Button(window1, text = "OK", font = ("Times", 15), borderwidth = 10, command = encode).place(x = 120, y = 490)
	butback1 = Button(window1, text = "Back", font = ("Times", 15), borderwidth = 10, command = main).place(x = 420, y = 490)
	window1.mainloop()

def close(e = None) :
	global window, window1, window2, window_width, window_height, x, y
	window.destroy()
	window1.destroy()
	window2.destroy()

def main(e = None) :
	global window, window1, window2, window_width, window_height, x, y
	window.state("normal")
	window.config(background = "#9068C7")
	window1.state("iconic")
	window1.config(background = "#9068C7")
	window2.state("iconic")
	window2.config(background = "#9068C7")
	window.title("Image Steganography")
	window.geometry(f"{window_width}x{window_height}+{x}+{y}")
	label10 = Label(window, text = "Main Menu", font = ("Arial Black", 20), bg = "#9068C7").place(x = 325, y = 50)
	butencode = Button(window, text = "Encode", bg = "red", activebackground = "orange", borderwidth = 10, font = ("Times", 20), command = file_details_for_encoding).place(x = 350, y = 150)
	butdecode = Button(window, text = "Decode", bg = "cyan", activebackground = "skyblue", borderwidth = 10, font = ("Times", 20), command = file_details_for_decoding).place(x = 350, y = 270)
	butclose = Button(window, text = "Close", borderwidth = 10, font = ("Times", 20), command = close).place(x = 360, y = 390)
	window.mainloop()

path1 = path2 = msg = fileAddress1 = fileAddress2 = " "
window_width = 600
window_height = 600
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight() - 55
x = int(screen_width / 2 - window_width / 2)
y = int(screen_height / 2 - window_height / 2)
frame = Frame(window, width = 200, height = 600, bg = "#5A24A4").pack(side = LEFT)
label = Label(window, text = "Image\nSteganography", font = ("Times", 22, "bold", "italic"), fg = "yellow", bg = "#5A24A4").place(x = 7, y = 263)
frame1 = Frame(window1, width = 600, height = 100, bg = "#5A24A4").pack(side = TOP)
label1 = Label(window1, text = "Encode", font = ("Times", 22, "bold", "italic"),fg = "yellow", bg = "#5A24A4").place(x = 257, y = 33)
frame2 = Frame(window2, width = 600, height = 100, bg = "#5A24A4").pack(side = TOP)
label2 = Label(window2, text = "Decode", font = ("Times", 22, "bold", "italic"),fg = "yellow", bg = "#5A24A4").place(x = 257, y = 33)
window1.bind("<Return>", encode)
window2.bind("<Return>", decode)
window.bind("<Escape>", close)
window1.bind("<Escape>", close)
window2.bind("<Escape>", close)
main()