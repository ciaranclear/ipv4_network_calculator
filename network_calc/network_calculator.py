from ipv4_networks.ipv4_networks import make_networks




if __name__ == "__main__":

    networks = [
        ["A network",62],
        ["B network",62],
        ["C network",62],
        ["D network",67]
    ]

    networks1 = [
        ["A",127],
        ["B",126]
    ]

    networks = make_networks(networks, "192.168.0.0", "255.255.255.0", True)
    for name, network in networks.items():
        print(f"{'#'*40}")
        print(name)
        print(network)
