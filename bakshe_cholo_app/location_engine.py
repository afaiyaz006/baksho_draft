from tkinter import E
import osmnx as ox
import networkx as nx
import os
import folium
class LocationWorker:
    '''
        Location API for easy interfacing
    '''
    def __init__(self,mode:str,optimizer:str):
        ox.config(log_console=True,use_cache=True)
        self.mode=mode
        self.optimizer=optimizer
        self.file_path=os.path.dirname(os.path.realpath('osm_files/UAP_To_Farmgate.osm'))+"\\UAP_To_Farmgate.osm"
        self.graph=ox.graph_from_xml(self.file_path,simplify=True,retain_all=False)

    def calculate_shorted_distance(self,loc_a,loc_b):
        try:
            loc_a_node=ox.nearest_nodes(self.graph,loc_a[0],loc_a[1])
            loc_b_node=ox.nearest_nodes(self.graph,loc_b[0],loc_b[1])
        
            shortest_route = nx.shortest_path(self.graph,
                                  loc_a_node,
                                  loc_b_node,
                                  weight=self.optimizer)
        except:
            return None
        return shortest_route
    
    def make_route(self,shortest_routes):
        
        if len(shortest_routes)>0:
            map=None
            try:
                map=ox.plot_route_folium(self.graph,shortest_routes[0])
            except:
                print("Shortest path not found")
            for i in range(1,len(shortest_routes)):
                try:
                    map = ox.plot_route_folium(self.graph,shortest_routes[i],route_map=map)
                except:
                    print("Shortest route not found!")

            return map
        else:
            return None
    def get_graph(self):
        return self.graph

