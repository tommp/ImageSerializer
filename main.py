#!/usr/bin/python
try:
	from Tkinter import *
except:
	print "ERROR: Tkinter is not installed, install packages python-tk idle python-pmw python-imaging (sudo apt-get install for linux)"


class ImageSerializer(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.pixelscale=10
		self.num_pixels=10
		self.title("Canvas")
		self.status_text=StringVar()
		self.letter_matrix = [[0 for x in range(self.num_pixels)] for y in range(self.num_pixels)] 
		self.symbol_values = {}

		self.fill_symbol_dict()

		self.symbol_input = Entry(self, width=3, justify="center")
		self.text_disp = Label(self, textvariable=self.status_text, text="Errorlog")
		self.text_symbol_input = Label(self, text="Symbol value:")
		self.canvas = Canvas(self, 
			width=self.pixelscale*self.num_pixels, 
			height=self.pixelscale*self.num_pixels, 
			cursor="cross", 
			bg="#fff")

		menubar = Menu(self)
		menubar.add_command(label="Save", command=self.save_data)
		menubar.add_command(label="Clear canvas", command=self.clear_canvas)
		menubar.add_command(label="Clear all", command=self.clear_all)
		menubar.add_command(label="Quit", command=self.quit)

		self.canvas.bind("<B1-Motion>", self.dragging)
		self.canvas.bind("<ButtonPress-1>", self.dragging)

		self.canvas.pack(side="left")
		self.text_symbol_input.pack(side="top")
		self.symbol_input.pack(side="top")
		self.text_disp.pack(side="bottom")

		self.config(menu=menubar)

	def fill_symbol_dict(self):
		try:
			data_file = open("letter_values.txt","r")
		except:
			self.status_text.set("ERROR:Failed to open file letter_values.txt")
		for line in data_file:
			number_value = ""
			for x in range(len(line)-1):
				number_value += line[x+1]
			self.symbol_values[line[0]] = number_value

	def hello(self):
		print "hello"

	def dragging(self, event):
		self.letter_matrix[event.x / self.pixelscale][event.y / self.pixelscale] = 1
		x0,y0 = (event.x, event.y)
		self.canvas.create_rectangle(x0-self.pixelscale,
						y0-self.pixelscale,
						x0+self.pixelscale,
						y0+self.pixelscale, 
						fill="black")

	def save_data(self):
		try:
			data_file = open("training_data.txt", 'a')
		except:
			self.status_text.set("ERROR:Failed to open file training_data.txt")
			return -1

		string = self.symbol_input.get()
		value = self.symbol_values[string]
		letter_mask = ""

		for x in range(self.num_pixels):
			for y in range(self.num_pixels):
				letter_mask += str(self.letter_matrix[x][y])

		if len(string) > 1:
			self.status_text.set("ERROR: String too long!")
		else:
			data_file.write(letter_mask + '\n')
			data_file.write(value)
			self.status_text.set(string + " saved!")

		data_file.close()

	def clear_canvas(self):
		for x in range(self.num_pixels): 
			for y in range(self.num_pixels):
				self.letter_matrix[x][y] = 0
		self.canvas.delete("all")
		self.status_text.set("Cleared canvas!")

	def clear_all(self):
		for x in range(self.num_pixels): 
			for y in range(self.num_pixels):
				self.letter_matrix[x][y] = 0
		self.canvas.delete("all")
		self.symbol_input.delete(0,"end")
		self.status_text.set("Cleared all!")

if __name__ == "__main__":
	app = ImageSerializer()
	app.mainloop()