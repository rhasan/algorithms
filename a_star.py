
INPUT_GRAPH_LOCATION = "romania.in"


def get_input_graph(file):

    input_graph_file = open(file,"r")
    
    first_line = next(input_graph_file)

    (n,m) = map(int,first_line.split())
    print n, m

    line_count = 0
    for line in input_graph_file:

        (node_label,geo_location) = line.split("=")
        node_label = node_label.strip()
        (geo_x,geo_y) = map(int,geo_location.split(","))
        print "Node:["+node_label+"], geo x:", geo_x, "geo y:", geo_y
        line_count += 1
        if(line_count==n):
            break;

    line_count = 0
    for line in input_graph_file:
        (u_node_label,edges) = line.split(":")
        u_node_label = u_node_label.strip()

        edge_list = edges.split(",")

        print "Node:["+u_node_label+"] has edges:"
        for edge in edge_list:
            (v_node_label,cost) = edge.strip().split("=")
            v_node_label = v_node_label.strip()
            cost = int(cost)
            print "["+v_node_label+"]", "cost:",cost

        if(line_count==m):
            break;

def main():
    get_input_graph(INPUT_GRAPH_LOCATION)


if __name__ == "__main__":
    main()