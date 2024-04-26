class StatsPlot:
    def __init__(self, canvas):
        self.canvas = canvas

    def plot(self, stats):
        self.canvas.delete('all')
        h = stats.get_height()
        bw = 512 / h
        max_layer_count = max(stats.counts)
        lh = 128/max_layer_count
        for i in range(h):
            total = stats.counts[i]
            blue_leaves = stats.get_leaf_count(i, False)
            red_leaves = stats.get_leaf_count(i, True)
            self.canvas.create_rectangle(i*bw, 128, (i+1)*bw, 128-total*lh, fill='green')
            self.canvas.create_rectangle(i*bw, 128, i*bw + bw/2, 128-blue_leaves*lh, fill='blue')
            self.canvas.create_rectangle(i*bw+bw/2, 128, (i+1)*bw, 128-red_leaves*lh, fill='red')
            self.canvas.create_text(i*bw+bw/2, 138, text=f"1/{2**i}")
            self.canvas.create_text(i*bw+bw/2, 148, text=f"{total}")
            self.canvas.create_text(i*bw+bw/2, 158, text=f"{blue_leaves}", fill='blue')
            self.canvas.create_text(i*bw+bw/2, 168, text=f"{red_leaves}", fill='red')
