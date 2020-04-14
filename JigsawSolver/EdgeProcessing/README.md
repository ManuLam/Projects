# Jigsaw Solver - 4th Year Project (CS440)

## Goal 
- Enrichment of Jigsaw Pieces with Computer Vision
- Solving Jigsaw Puzzles by Shape with Computer Vision


# Modules
## canny_edge.py
    This is one of the first modules implemented, canny_edge includes algorithms that
    extracts Jigsaw pieces from an image and also applies the edge dectector algorithm ontop
    
## harris_corner.py
    This module honestly has too much inside it, I didn't refactor it enough.
    It includes most of our method calls.
    It includes the HarrisCorner algorithm, Maximum rectangle algorithm and creates the
    jigsaw pieces and then enriches them with classifiers.
    
## compute_sides.py
    Includes logic for classifying a piece and then enriching them with colour.
   
## hough_lines_p.py
    This module includes the line dectection algorithms for determine if an edge is flat
   
## jigsaw_solver.py
    This module includes all the solving logic, matching and combinatorial. 

## jigsaw_visualizer.py
    This module includes all the visualising canvas and templates used to show
    the entire progress of our piece enrichment process, and allows us to see
    the jigsaw in a puzzle box
    
## JigsawPiece.py
    A JigsawPiece class that allows us to objectise from an image to a Python object
    to later be manipulated.