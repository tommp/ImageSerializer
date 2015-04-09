#!/usr/bin/python
try:
	from Tkinter import *
except:
	print "ERROR: Tkinter is not installed, install packages python-tk idle python-pmw python-imaging (sudo apt-get install for linux)"


class ImageSerializer(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.pixelscale=10
		self.num_pixels=20
		self.title("Canvas")
		self.status_text=StringVar()
		self.letter_matrix = [[-0.5 for x in range(self.num_pixels)] for y in range(self.num_pixels)] 
		self.symbol_values = {}

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


	def hello(self):
		print "hello"

	def dragging(self, event):
		self.letter_matrix[event.x / self.pixelscale][event.y / self.pixelscale] = 0.5
		x0,y0 = (event.x, event.y)
		self.canvas.create_rectangle(x0-self.pixelscale,
						y0-self.pixelscale,
						x0+self.pixelscale,
						y0+self.pixelscale, 
						fill="black")

	def save_data(self):
		try:
			data_file = open("training_data.txt","rw")
		except:
			self.status_text.set("ERROR:Failed to open file!")
			return -1

		string=self.symbol_input.get()
		if len(string) > 1:
			self.status_text.set("ERROR: String too long!")
		else:
			self.status_text.set(string + " saved!")

		data_file.close()

	def clear_canvas(self):
		for x in range(self.num_pixels): 
			for y in range(self.num_pixels):
				self.letter_matrix[x][y] = -0.5
		self.canvas.delete("all")
		self.status_text.set("Cleared canvas!")

	def clear_all(self):
		for x in range(self.num_pixels): 
			for y in range(self.num_pixels):
				self.letter_matrix[x][y] = -0.5
		self.canvas.delete("all")
		self.symbol_input.delete(0,"end")
		self.status_text.set("Cleared all!")

if __name__ == "__main__":
	app = ImageSerializer()
	app.mainloop()