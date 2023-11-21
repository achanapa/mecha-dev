import bpy
import json
from typing import List

# Reads bolt parameters from a JSON file.
# Return size of head_type, bit_type, head_length, head_dia, thread_length, thread_dia and space_length
def input_DataSize(path_to_datafile):
    with open(path_to_datafile, 'r') as openfile:
        json_object = json.load(openfile)        
        head_length = json_object["Head_Length"]
        head_dia = json_object["Head_Diameter"]
        thread_length = json_object["Thread_Length"]
        thread_dia = round(json_object["Thread_Diameter"])
        space_length = json_object["Space_Length"]
        head_type = json_object["type_head"]
        bit_type = json_object["type_bit"]
    return head_type, bit_type, head_length, head_dia, thread_length, thread_dia, space_length

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# This class use the data size to build a bolt with addon BoltFactory.
class BuildaBolt:
    def __init__(self, head_type, bit_type, head_length, head_dia, thread_length, thread_dia, space_length, path_to_savefile):
      self.bf_Model_Type = 'bf_Model_Bolt'   
      self.bf_Head_Type = head_type          #select on UI
      self.bf_Bit_Type = bit_type            #select on UI
      self.bf_Shank_Length = space_length    #grid length
      self.bf_Shank_Dia = thread_dia         #grid diameter
      self.bf_Hex_Head_Height = head_length  #head length    
      self.bf_Hex_Head_Flat_Distance = head_dia    #head radius
      self.bf_CounterSink_Head_Dia = head_dia      #head radius
      self.bf_Cap_Head_Height = thread_dia  #head length 
      self.bf_Cap_Head_Dia = head_dia       #head diameter
      self.bf_Dome_Head_Dia = head_dia      #head diameter
      self.bf_Pan_Head_Dia = head_dia       #head diameter
      self.bf_Thread_Length = thread_length #thread length
      self.bf_Major_Dia = thread_dia        #thread length
      self.bf_Crest_Percent = 10            #thread length
      self.bf_Root_Percent = 10             #thread length
      self.bf_Div_Count = 36                #thread length
      self.path_to_savefile = path_to_savefile

    # This function map the size of major diameter of bolt to the minor diameter and pitch of bolt.
    def size_thread(self):
        thread_pitch = {'M2': 0.4, 'M3': 0.5, 'M4': 0.7, 'M5': 0.8, 'M6': 1, 'M8': 1.25, 'M10': 1.5, 'M12': 1.75, 'M14': 2, 'M16': 2}
        thread_minor = {'M2': 1.6, 'M3': 2.5, 'M4': 3, 'M5': 4, 'M6': 5, 'M8': 6, 'M10': 8, 'M12': 10, 'M14': 12, 'M16': 14}   
        boltM = 'M' + str(self.bf_Major_Dia)
        pitch = thread_pitch[boltM]                
        minor = thread_minor[boltM]
        return pitch, minor

    # This function map the name of head od bolt to the size of component for eachtype.   
    def size_head(self):
        #head_length = M size
        #Allen[depth, dist]
        Allen_bit = {'M2':[1.6, 2.5],
                    'M3':[1.6, 2.5], 'M4':[2.2, 3], 'M5':[2.5, 4], 
                    'M6':[3, 5], 'M8':[4, 6], 'M10':[5, 8],
                    'M12':[6, 10], 'M14':[7, 12], 'M16':[8, 14]}
        #Torx[depth, size]
        Torx_bit = {'M2':[1.3, 10],
                    'M3':[1.3, 10], 'M4':[1.6, 20], 'M5':[2, 25], 
                    'M6':[3.0, 30], 'M8':[3.3, 40], 'M10':[4.5, 50],
                    'M12':[5.2, 55], 'M14':[5.2, 55], 'M16':[5.2, 55]}
                    
        #Phillips[depth, dia]
        Phillips_bit = {'M2':[1.75, 3.6],
                        'M3':[1.75, 3.6], 'M4':[2.3, 4.5], 'M5':[2.8, 5.1], 
                        'M6':[3.4, 6.7], 'M8':[4.4, 8.4], 'M10':[5.7, 10],
                        'M12':[5.7, 10], 'M14':[5.7, 10], 'M16':[5.7, 10]}
                        
        if self.bf_Head_Type == 'HEX':
            Head_Type = 'bf_Head_Hex'
        elif self.bf_Head_Type == 'CAP':
             Head_Type = 'bf_Head_Cap'
        elif self.bf_Head_Type == 'DOME':
             Head_Type = 'bf_Head_Dome'
        elif self.bf_Head_Type == 'PAN':
             Head_Type = 'bf_Head_Pan'
        elif self.bf_Head_Type == 'COUNTERSINK':
             Head_Type = 'bf_Head_CounterSink'
            
        
        boltM = 'M' + str(self.bf_Major_Dia)
        if self.bf_Bit_Type == 'ALLEN':
            Bit_Type = 'bf_Bit_Allen'
            depth = Allen_bit[boltM][0] 
            size_float = Allen_bit[boltM][1]
            size_str = "bf_Torx_T10" 
            
        elif self.bf_Bit_Type == 'TORX':
            Bit_Type ='bf_Bit_Torx'
            depth = Torx_bit[boltM][0]
            size_float = Torx_bit[boltM][1]
            size_str = "bf_Torx_T" + str(Torx_bit[boltM][1])
            
        elif self.bf_Bit_Type == 'PHILLIPS':
            Bit_Type ='bf_Bit_Phillips'
            depth = Phillips_bit[boltM][0]
            size_float = Phillips_bit[boltM][1]
            size_str = "bf_Torx_T10" 
            
        else:
            Bit_Type ='bf_Bit_None'
            depth = 0
            size_float = 0
            size_str = "bf_Torx_T10" 
        return Head_Type, Bit_Type, depth, size_float, size_str
        
    # This function add the bolt by mesh using the mapping size
    def addBolt(self):
        pitch, minor = self.size_thread()
        Head_Type, Bit_Type, depth, size_float, size_str = self.size_head()                                            
        bpy.ops.mesh.bolt_add(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), change=True, 
                                            bf_Model_Type = self.bf_Model_Type ,   
                                            bf_Head_Type = Head_Type,    
                                            bf_Bit_Type = Bit_Type,       
                                            bf_Shank_Length = self.bf_Shank_Length,            
                                            bf_Shank_Dia = self.bf_Shank_Dia,                
                                            bf_Phillips_Bit_Depth = depth,  
                                            bf_Allen_Bit_Depth = depth,          
                                            bf_Allen_Bit_Flat_Distance = size_float,   
                                            bf_Torx_Size_Type = size_str,            
                                            bf_Torx_Bit_Depth = depth,               
                                            bf_Hex_Head_Height = self.bf_Hex_Head_Height,            
                                            bf_Hex_Head_Flat_Distance = self.bf_Hex_Head_Flat_Distance,   
                                            bf_CounterSink_Head_Dia = self.bf_CounterSink_Head_Dia,        
                                            bf_Cap_Head_Height = self.bf_Cap_Head_Height,         
                                            bf_Cap_Head_Dia = self.bf_Cap_Head_Dia,        
                                            bf_Dome_Head_Dia = self.bf_Dome_Head_Dia,           
                                            bf_Pan_Head_Dia = self.bf_Pan_Head_Dia,           
                                            bf_Philips_Bit_Dia = size_float,         
                                            bf_Thread_Length = self.bf_Thread_Length,           
                                            bf_Major_Dia = self.bf_Major_Dia,          
                                            bf_Pitch = pitch,                    
                                            bf_Minor_Dia = minor,             
                                            bf_Crest_Percent = 10,            
                                            bf_Root_Percent = 10,            
                                            bf_Div_Count = 36)              

    # This function export the object as a glb format to the assign path_to_savefile. 
    def exportBolt(self):
        for obj in bpy.context.scene.objects:
            obj.select_set(True)
        bpy.ops.export_scene.gltf(
            filepath = self.path_to_savefile,
            export_format='GLB',
            export_apply=True,  # Apply modifiers
            export_colors=True,  # Export vertex colors
            export_normals=True,  # Export normals
            export_cameras=True,  # Export cameras
            export_lights=True,  # Export lights
            export_yup=True  # Y-axis up
        )

if __name__ == '__main__':
    path_to_savefile ="./3DModel/save_bolt.glb" 
    path_to_datafile='./data_size.json'
    head_type, bit_type, head_length, head_dia, thread_length, thread_dia, space_length = input_DataSize(path_to_datafile)
    b1 = BuildaBolt(head_type, bit_type, head_length, head_dia, thread_length, thread_dia, space_length, path_to_savefile)
    b1.addBolt()
    b1.exportBolt()
    
 



