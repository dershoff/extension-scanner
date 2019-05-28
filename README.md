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


## Example
</br>es = ExtensionScanner()
</br>es.set_search_path( '/media/dmitry/Data/Docs/recovering_files/recovered' )
</br>es.set_storage_path( '/media/dmitry/Data/Docs/recovering_files/test' )
</br>es.scan_all_extensions()
</br>es.run( ['pdf', 'doc'], action='scan' )


## Or more explicitly:
</br>s.add_target_extensions( ['pdf', 'csv' ])
</br>s.set_action( 'copy' )
</br>s.process()


