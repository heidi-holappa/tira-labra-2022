import matplotlib.pyplot as pyplt

class GraphManagement:

    def __init__(self, x_axis: list, y_axis: list, labels: list = []):
        self.x_values = x_axis
        self.y_values = y_axis
        self.labels = labels

    def construct_line_graph(self):
        pyplt.plot(self.x_values, self.y_values)
        pyplt.xlabel("x-axis")
        pyplt.ylabel("y-axis")
        pyplt.title("title")
        # pyplt.savefig("line-graph.png")
        pyplt.show()
    
    def construct_bar_chart(self):
        bar_labels = self.labels
        pyplt.bar(
            self.x_values,
            self.y_values,
            tick_label= bar_labels,
            width=0.8,
            color = ["#e50053", "#255cae"]
            )
        pyplt.xlabel("x-axis")
        pyplt.ylabel("y-axis")
        pyplt.title("title")
        # pyplt.savefig("bar-chart-1.png")
        pyplt.show()
        


if __name__ == "__main__":
    graphbuilder = GraphManagement([1,2,3, 4, 5, 6], [6, 4, 5, 10, 2, 3])
    graphbuilder.construct_line_graph()
    graphbuilder.labels = ["Ducks", "Pigs", "Cows"]
    graphbuilder.construct_bar_chart()