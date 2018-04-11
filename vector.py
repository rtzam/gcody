# Numpy wrappers to abstract memory management for numpy arrays

# imports ----------------------------------------------------
import numpy as np

# vector classes -------------------------------------------

# a wrapper over the numpy array for numerical values
class vec():
    
    def __init__(self, data=None, length=None, mem_scale=2, data_type=np.float64):
        
        '''
        creates an array,shape of array, dimention of array, length of array
        wrapper over numpy array to abstract away memory management
        '''
        
        # assigning data_type to attribute
        if data_type:
            self.data_type = np.dtype(data_type)
            
        # number that memory is scaled when size expands
        if mem_scale <= 1:
            raise ValueError('mem_scale must be greater than 1')
        self.mem_scale = mem_scale         
        
        # if an array is given then 
        if type(data) != type(None):
            
            # reasssinging data type
            self.data_type = np.dtype(type(data[0]))
            
            
            # shape of the block with assigned values
            self._real_length = len(data) 
            
            # create new indicies
            temp_len = int(np.ceil(self.mem_scale*self._real_length))   
            
            # creates hidden array          
            self._array = np.zeros(temp_len).astype(self.data_type) 
            self._array[0:len(data)] = data # fills preallocated array
            
            # records hidden array length
            self._length = len(self._array) # private length 
            
            return
        
        else:
            # creates an empty vector
            self._real_length = 0
    
            # create new indicies
            temp_len = int(np.ceil(self.mem_scale*length))
                
            # creates hidden array
            self._array = np.zeros(temp_len).astype(self.data_type) # creates the larger preallocated block
            
            # records hidden array length
            self._length = len(self._array) # private length 
            
            # end of init
            return
        
    # function that handles the memory allocation of append
    def append(self, x):
        
        if type(x) == int or type(x) == float or type(x) == str:
            
            if self._length > self._real_length:
                # adds a single value to the end of the array
                self._array[self._real_length] = x
                self._real_length += 1
                
                # end of append
                return
                
            else: # self._length[axis] == self._real_length[axis]:
                # preallocated array and real array are same size 
                # must increase preallocation size
                
                # storing allocated memory
                temp = self._array[0:self._real_length]
                
                # creating new array length
                self._length = int(np.ceil(self.mem_scale*self._length))
                
                # preallocating new hidden array
                self._array = np.zeros(self._length).astype(self.data_type)
                
                # copying values to hidden array
                self._array[0:self._real_length] = temp
                
                # appending new value and adjusting parameters
                self._array[self._real_length] = x
                
                # updating real_length
                self._real_length += 1
                
                # end of append
                return
            
        # appending an array
        else:
            
            # simple appending array
            if self._length > self._real_length + len(x):
                
                # adds a single value to the end of the array
                self._array[self._real_length:self._real_length+len(x)] = x
                self._real_length += len(x)
                
                # end of append
                return     
            
            else:
                # preallocated array and real array are same size 
                # must increase preallocation size
            
                # storing allocated memory
                temp = self._array[0:self._real_length]
            
                # ensuring enough memory is created creating new length
                self._length = int(np.ceil(self.mem_scale*(self._real_length+len(x))))
            
                # preallocating new hidden array
                self._array = np.zeros(self._length).astype(self.data_type)
            
                # copying values to hidden array
                self._array[0:self._real_length] = temp
            
                # appending new value and adjusting parameters
                self._array[self._real_length : self._real_length+len(x)] = x
            
                # updating real_length
                self._real_length += len(x)
                
                # end of append
                return                          
          
    # gives returns the real array
    def data(self):
        return self._array[0:self._real_length]
            
        
    # repr and str give the string representations 
    def __repr__(self):
        return str(self._array[0:self._real_length])
    
    def __str__(self):
        return str(self._array[0:self._real_length])
    
    # allows for [] indexing
    def __getitem__(self, index):
        
        indices = 0
        if isinstance(index, slice):
            indices = index.indices(index.stop)
            indices = np.array(indices, dtype=int)
        
        # single value case
        if isinstance(index, int):
            
            # index is in length of real array
            if index < self._real_length:
                return self._array[index]  
            else:
                raise ValueError('Index is out or array range')
        
        else:
            
            if np.all(indices < self._real_length):
                return self._array[index]
            else:
                raise ValueError('Index is out or array range')
            
            
    
    


# a two dimentional numeical vector
class vec2d():
    
    def __init__(self, data=None, shape=None, mem_scale=2, datatype=np.float64):
        '''
        > DATA is a 2D array
        > SHAPE is the shape of a preallocated array
        
        '''
        
        # assigning data_type to attribute
        if datatype:
            self.datatype = np.dtype(datatype)
            
        # number that memory is scaled when size expands
        if mem_scale <= 1:
            raise ValueError('mem_scale must be greater than 1')
        self.mem_scale = mem_scale         
        
        # if an array is given then 
        if type(data) != type(None):
            
            # reasssinging data type
            self.data_type = np.dtype(type(data[0]))
            
            # shape of the block with assigned values
            self._real_shape = np.array(np.array(data).shape)
            
            # create new indicies
            temp_shape = np.ceil(self.mem_scale*self._real_shape).astype(int)
            
            # creates hidden array          
            self._array = np.zeros(temp_shape).astype(self.datatype) 
            
            # fills preallocated array
            self._array[0:self._real_shape[0], 0:self._real_shape[1]] = data 
            
            # records hidden array length
            # private shape
            self._length = np.array(self._array.shape)
            
            return
        
        else:
            
            if shape:
                # creates a zeros based on shape
                self._real_shape = np.array(shape)
            else:
                # creates an empty vector
                self._real_shape = np.array((0, 0))
        

        # creating hidden array shape if real shape is 0,0
        if np.all(self._real_shape == np.array((0, 0))):
            # create new indicies
            temp_shape = np.ceil(self.mem_scale*np.array((1,1))).astype(int)

        # case where a single dimension size is given
        elif np.any(self._real_shape == 0.0):
            temp_shape =  np.ceil(self.mem_scale*(self._real_shape+1)).astype(int)
            
        else:
            # create new indicies
            temp_shape= np.ceil(self.mem_scale*self._real_shape).astype(int)
            
        
        
        
        # creates hidden array
        self._array = np.zeros(temp_shape).astype(self.datatype) # creates the larger preallocated block
        
        # records hidden array length
        self._shape = self._array.shape # private length 
        
        # end of init
        return   
    
    def append(self, x, dim=0): # append to row as default
        
        # convert input data 
        x = np.array(x).astype(self.datatype)
        
        # appends a single vector
        
        if len(x.shape) == 1:
            
            # enough memory
            if self._real_shape[dim] < self._shape[dim]:
                
                if dim == 0:
                    # appends a new row
                    
                    self._array[self._real_shape[0], 0:self._real_shape[1]] = x
                    # updates shape
                    self._real_shape[0] += 1
                else:
                    # appends a new column
                    self._array[0:self._real_shape[0], self._real_shape[1]] = x
                    # updates shape
                    self._real_shape[1] += 1
            
            # not enough memory
            else:
                
                # if dimension is row
                if dim == 0:
                    
                    # copies old array
                    temp_array = self._array[0:self._real_shape[0], 0:self._real_shape[1]]
                    
                    # creates new shape
                    self._shape = [np.ceil(self.mem_scale*self._shape[0]).astype(int), self._shape[1]]
                    
                    # creates new array
                    self._array = np.zeros(self._shape).astype(self.datatype)

                    # copying over old data
                    self._array[0:self._real_shape[0],0:self._real_shape[1]] = temp_array
                    
                    # appends a new row
                    self._array[self._real_shape[0], 0:self._real_shape[1]] = x
                    
                    # updates shape
                    self._real_shape[0] += 1  
                    
                    return
                    
                elif dim == 1: # dimension is column
                    
                    # copies old array
                    temp_array = self._array[0:self._real_shape[0], 0:self._real_shape[1]]
                
                    # creates new shape
                    self._shape = [self._shape[0], np.ceil(self.mem_scale*self._shape[1]).astype(int)]
                
                    # creates new array
                    self._array = np.zeros(self._shape).astype(self.datatype)

                    # copying over old data
                    self._array[0:self._real_shape[0],0:self._real_shape[1]] = temp_array
                
                    # appends a new column
                    self._array[0:self._real_shape[0], self._real_shape[1]] = x
                
                    # updates shape
                    self._real_shape[1] += 1
                    
                    return
                
        # appending a block    
        else:
            
            # enough memory
            if self._real_shape[dim] + x.shape[dim] < self._shape[dim]:
                
                if dim == 0:
                    # appends a new row block
                    
                    self._array[self._real_shape[0]:self._real_shape[0]+x.shape[0], 0:self._real_shape[1]] = x
                    # updates shape
                    self._real_shape[0] += 1
                else:
                    # appends a new column block to the column
                    self._array[0:self._real_shape[0], self._real_shape[1]:self._real_shape[1]+x.shape[1]] = x
                    # updates shape
                    self._real_shape[1] += 1
            
            # not enough memory
            else:
                
                # is dimension is row
                if dim == 0:
                    
                    # copies old array
                    temp_array = self._array
                    
                    # creates new shape
                    self._shape = np.ceil(self.mem_scale*(self._shape[0]+x.shape[0])).astype(int)
                    
                    # creates new array
                    self._array = np.zeros(self._shape).astype(self.datatype)
                    
                    # appends a new row
                    self._array[self._real_shape[0]:self._real_shape[0]+x.shape[0], 0:self._real_shape[1]] = x
                              
                    # updates shape
                    self._real_shape[0] += 1  
                    
                    return
                    
                elif dim == 1: # is dimension is column
                    
                    # copies old array
                    temp_array = self._array
                
                    # creates new shape
                    self._shape = np.ceil(self.mem_scale*(self._shape[1]+x.shape[1])).astype(int)
                
                    # creates new array
                    self._array = np.zeros(self._shape).astype(self.datatype)
                
                    # appends a new column
                    self._array[0:self._real_shape[0], self._real_shape[1]:self._real_shape[1]+x.shape[1]] = x
                
                    # updates shape
                    self._real_shape[1] += 1
                    
                    return
                    
                    
    # gives returns the real array
    def data(self):
        return self._array[0:self._real_shape[0], 0:self._real_shape[1]]
            
        
    # repr and str give the string representations 
    def __repr__(self):
        return str(self._array[0:self._real_shape[0], 0:self._real_shape[1]])
    
    def __str__(self):
        return str(self._array[0:self._real_shape[0], 0:self._real_shape[1]])
    
    # allows for [] indexing
    def __getitem__(self, index):
        
        # single value case
        if isinstance(index, int):
            # an int gives a square vector of that int
            return self._array[0:index, 0:index]

        # See if there is a better way to do this
        elif isinstance(index, slice):
            # only slice with nonetype elements are allowed
            flat = self._array[0:self._real_shape[0],0:self._real_shape[1]].flatten()

            return flat[index]
            
        # handling many cases of tuple instance of index
        elif isinstance(index, tuple):

            # checking if any indecies are ints
            if isinstance(index[0],int) and isinstance(index[1],int):
                # checking if int is in range
                if index[0] <= self._real_shape[0]:
                    if index[1] <= self._real_shape[1]:
                        return self._array[index]
                    else:
                        raise ValueError('Invalid Second Index')
                    
                else:
                    raise ValueError('Invalid First Index')

            # case where first index is an int and second index is a slice
            elif isinstance(index[0],int) and isinstance(index[1],slice):
                # checking if int is in range
                if index[0] <= self._real_shape[0]:

                    # return a row and all columns
                    if index[1].stop == None:
                        return self._array[index[0], 0:self._real_shape[1]]

                    # return a row and some columns
                    elif index[1].stop <= self._real_shape[1]:
                        return self._array[index]
                    else:
                        raise ValueError('Invalid Second Index')
                    
                else:
                    raise ValueError('Invalid First Index')

            # case where second index is an int and first index is a slice
            elif isinstance(index[1],int) and isinstance(index[0],slice):
                # checking if int is in range
                if index[1] <= self._real_shape[1]:

                    # return all rows and a columns
                    if index[0].stop == None:
                        return self._array[0:self._real_shape[0],index[1]]

                    # reutrn some rows and a column
                    elif index[0].stop <= self._real_shape[0]:
                        return self._array[index]
                    else:
                        raise ValueError('Invalid First Index')
                    
                else:
                    raise ValueError('Invalid Second Index')
            

            # First index is everything
            if index[0].start == None:

                # return whole array
                if index[1].start == None:
                    return self._array[0:self._real_shape[0],0:self._real_shape[1]]
                
                else:
                    # return part of array. All rows, some columns
                    if index[1].stop <= self._real_shape[1]:                        
                        return self._array[0:self._real_shape[0],index[1]]
                    else:
                        # second index is bad
                        raise ValueError('Invalid Second Index')

            # Second index is not everything
            elif index[1].start == None:
                
                # return part of array. some rows, all columns
                if index[0].stop <= self._real_shape[0]:                        
                    return self._array[index[0], 0:self._real_shape[1]]
                else:
                    # second index is bad
                    raise ValueError('Invalid First Index')
            
            # case where neither indicies are everything
            else:
                if index[0].stop <= self._real_shape[0]:
                    if index[1].stop <= self._real_shape[1]:
                        return self._array[index]
                    else:
                        raise ValueError('Invalid Second Index')
                else:
                    raise ValueError('Invalid First Index')
        
# end of vec2D
