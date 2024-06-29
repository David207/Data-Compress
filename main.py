import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import heapq
import collections
import math

# Shannon-Fano Algorithm
def shannon_fano_encoding(data):
    if len(data) == 0:
        return {}, ""
    
    frequency = collections.Counter(data)
    sorted_freq = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
    
    def recursive_shannon_fano(freq_list):
        if len(freq_list) == 1:
            return {freq_list[0][0]: "0"}
        
        total = sum(item[1] for item in freq_list)
        cumulative = 0
        for i, item in enumerate(freq_list):
            cumulative += item[1]
            if cumulative >= total / 2:
                break
        
        left = recursive_shannon_fano(freq_list[:i+1])
        right = recursive_shannon_fano(freq_list[i+1:])
        
        encoding = {}
        for char, code in left.items():
            encoding[char] = "0" + code
        for char, code in right.items():
            encoding[char] = "1" + code
        
        return encoding
    
    encoding = recursive_shannon_fano(sorted_freq)
    encoded_data = "".join(encoding[char] for char in data)
    
    return encoding, encoded_data

# LZW Algorithm
def lzw_compression(data):
    max_table_size = pow(2, 16)
    table = {chr(i): i for i in range(256)}
    string = ""
    compressed_data = []
    code = 256
    
    for symbol in data:
        string_plus_symbol = string + symbol
        if string_plus_symbol in table:
            string = string_plus_symbol
        else:
            compressed_data.append(table[string])
            if len(table) <= max_table_size:
                table[string_plus_symbol] = code
                code += 1
            string = symbol
    
    if string in table:
        compressed_data.append(table[string])
    
    return compressed_data

# Huffman Algorithm
class HuffmanNode:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''
        
    def __lt__(self, other):
        return self.freq < other.freq

def huffman_encoding(data):
    if len(data) == 0:
        return {}, ""
    
    frequency = collections.Counter(data)
    heap = [HuffmanNode(freq, symbol) for symbol, freq in frequency.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        new_node = HuffmanNode(left.freq + right.freq, left.symbol + right.symbol, left, right)
        heapq.heappush(heap, new_node)
    
    root = heap[0]
    
    def build_codes(node, binary_string=''):
        if node is None:
            return {}
        if node.left is None and node.right is None:
            return {node.symbol: binary_string}
        
        codes = {}
        codes.update(build_codes(node.left, binary_string + '0'))
        codes.update(build_codes(node.right, binary_string + '1'))
        
        return codes
    
    huffman_codes = build_codes(root)
    encoded_data = ''.join(huffman_codes[char] for char in data)
    
    return huffman_codes, encoded_data

# Tkinter GUI
class CompressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compression Algorithms")
        
        self.input_label = tk.Label(root, text="Input Text:")
        self.input_label.pack()
        
        self.input_text = scrolledtext.ScrolledText(root, height=10)
        self.input_text.pack()
        
        self.shannon_button = tk.Button(root, text="Shannon-Fano Encode", command=self.shannon_fano)
        self.shannon_button.pack()
        
        self.lzw_button = tk.Button(root, text="LZW Encode", command=self.lzw)
        self.lzw_button.pack()
        
        self.huffman_button = tk.Button(root, text="Huffman Encode", command=self.huffman)
        self.huffman_button.pack()
        
        self.output_label = tk.Label(root, text="Encoded Output:")
        self.output_label.pack()
        
        self.output_text = scrolledtext.ScrolledText(root, height=10)
        self.output_text.pack()
    
    def shannon_fano(self):
        data = self.input_text.get("1.0", tk.END).strip()
        if not data:
            messagebox.showerror("Error", "Input text cannot be empty")
            return
        
        encoding, encoded_data = shannon_fano_encoding(data)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Encoding: {encoding}\n\nEncoded Data: {encoded_data}")
    
    def lzw(self):
        data = self.input_text.get("1.0", tk.END).strip()
        if not data:
            messagebox.showerror("Error", "Input text cannot be empty")
            return
        
        compressed_data = lzw_compression(data)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Compressed Data: {compressed_data}")
    
    def huffman(self):
        data = self.input_text.get("1.0", tk.END).strip()
        if not data:
            messagebox.showerror("Error", "Input text cannot be empty")
            return
        
        encoding, encoded_data = huffman_encoding(data)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Encoding: {encoding}\n\nEncoded Data: {encoded_data}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CompressionApp(root)
    root.mainloop()
