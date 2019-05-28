#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 13:21:13 2019

@author: Dmitry Ershov

A simple class that can iteratively search in subfolders for files with indicated extensions.
There is a set of actions on found files:
    - scan (simple search to test for presence)
    - copy
    - move
    - delete (to implement)
    
Convenient for extracting a lot of files with different extensions from a 
folder with unknown tree structure. For instance, an output of the program 
Photorec: many fodlers with 500 (mostly) meaningless file names.
If you want to extract from those folders all files like:
[*.pdf + *.cvs + *.jpeg]  - go for ExtensionScanner.
"""

import os, shutil
from collections import Counter


# TODO:
# it is better to keep the folders of the recofered files and the storage path separate.
# mp3 are recognized names: perhaps stored in the header.
# filter by size?
# filter by able to open/play?
# filter by equal entries?
# tags? 'uninteresting', 'interesting': apply action only to potentially interesting files?
# study interesting - if the target file found, then done. if not - copy the 'less interesting files.'
# implement action= 'delete'?
# implement overwrite_same_names    = False?
# implement: rcord source files? 
# IMPLEMENT some fields as private!!!!!!!!!!!!!!


class ExtensionScanner:
    
    search_path             = '' 
    storage_path            = ''
    target_extensions       = []
    extensions_typical      = ['gif', 'jpg', 'png', 'bmp', 'tif', 
                               'xcf', 'pcx', 'psd', 'ai', 'svg', 
                               'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx',               
                               'odt', 'odp', 'ods', 'rtf', 'csv', 'pdf',
                               'm4p', 'mp3', 'mp4', 'ogg', 'avi', 'wav',  'wma',  'mov', 'mpg',
                               'sh', 'blend' #'txt',
                               ]
    action                  = ''
    extensions_found        = []
    ready_to_run            = False
  
    
    def __init__(self ):
        self.action = 'scan'        
        
    def set_search_path(self, p):
        self.search_path = p
        
    def set_storage_path(self, p):
        self.storage_path = p    
        
    def add_target_extensions(self, exts ):
        if isinstance( exts, str):
            self.target_extensions.append( exts )
        elif isinstance( exts, list):
            self.target_extensions.extend( exts )
        
    def set_action(self, action):
        """
        action = 'scan', 'copy', 'move'
        """
        self.action = action
        
    def scan_all_extensions( self ):
        print('Search path: ')
        print( self.search_path )
        print( '\nScanning for extensions...' )

        # scan first to get all extensions:
        extensions_set          = set()
        extensions_counter      = Counter()

        for root, dirnames, filenames in os.walk( self.search_path ):    
            for file_full_name in filenames:        
                file_name, file_extension = os.path.splitext( file_full_name )
                file_extension = file_extension.lstrip('.')
                extensions_set.add( file_extension )
                extensions_counter.update( [file_extension] )

        self.extensions_found = list( extensions_set )
        
        print('\n')
        print( self.extensions_found )
        print('\n')
        print( extensions_counter )
        print( '\nFound %d extensions.'%len( self.extensions_found ) )
        
        
    def check(self):
        
        pref = '\nInterrputed :  '
        
        if self.action not in ['scan','copy','move']:
            self.ready_to_run = False            
            print( pref + 'Wrong action string.' )
            print( self.action )
            return       
        
        if not os.path.isdir( self.search_path ):
            self.ready_to_run = False
            print( pref + 'Search path does not exist.' )
            print( self.search_path  )
            return       
        
        if len( self.target_extensions ) == 0:            
            self.ready_to_run = False
            print( pref + 'Target extensions list is empty.')
            return 
        
        if self.action == 'copy' or  self.action == 'move':
            if not os.path.isdir( self.storage_path ):
                self.ready_to_run = False
                print( pref + 'Storage path does not exist.' )
                print( self.storage_path  )
                return
            
        self.ready_to_run = True
        
        
    def process(self, force_start_bool=False ):
        
        print(self)
        self.check()        
        
        if not self.ready_to_run:
            return     
        
        
        if force_start_bool:            
            z = 'y'
        else:
            z = input( 'Proceed? [n]/y: ' )
            
        if not(z=='y' or z=='Y'):
            print('Exit.')
            return
        
           
        print('\nProcessing...')
        
        c       = Counter()
        total   = 0
        overwritten = 0
        
        for root, dirnames, filenames in os.walk( self.search_path ):    
           
            for file_full_name in filenames:
                
                file_name, file_extension   = os.path.splitext( file_full_name )
                file_extension              = file_extension.lstrip('.')
                file_abs_path               = os.path.join( root, file_full_name )
                
                if  file_extension in self.target_extensions:
                    
                    file_dest_path = os.path.join( self.storage_path, file_full_name )                    
                    
                    # shutil.move( file_abs_path, s0 + f)        
                    if self.action == 'copy':
                        if os.path.isfile( file_dest_path ):
                            print(' File name already stored; Overwriting.')
                            #print( file_abs_path)
                            overwritten += 1
                        shutil.copy( file_abs_path, file_dest_path )

                    elif self.action == 'move':
                        shutil.copy( file_abs_path, file_dest_path )
                    elif self.action == 'scan':
                        pass
                        
                    total += 1
                    c.update( [file_extension] )
                    #print( file_abs_path )
                
                else:            
                    pass
        
        print( 'Found %s files.'%total )
        print( c ) 
        print( 'Overwritten files: %s'%overwritten )
        print('\nDone.')


    def __str__(self):  
        strout = ''        
        strout += '\nCurrent configuration:'
        strout += '\n   o Search path:'
        strout += '\n    ' + self.search_path
        strout += '\n   o Action:'
        strout += '\n    ' +  self.action  
        strout += '\n   o Targeted extensions:'
        strout += '\n    ' +  str( self.target_extensions )
        strout += '\n   o Storage path:'
        strout += '\n    ' +  self.storage_path        
        return strout
        
    def __repr__(self):  
        return self.__str__()
    
    def run(self, ext, action='scan' ):
        self.set_action( action )
        
        self.target_extensions = []
        self.add_target_extensions( ext )
        
        self.process( force_start_bool=True )

        

    
    

es = ExtensionScanner()

es.set_search_path( '/media/dmitry/Data/Docs/recovering_files/recovered' )
es.set_storage_path( '/media/dmitry/Data/Docs/recovering_files/test' )

es.scan_all_extensions()
es.run( ['pdf', 'doc'], action='scan' )

# or more explicitly:
# s.add_target_extensions( ['pdf', 'csv' ])
# s.set_action( 'copy' )
# s.process()

   


