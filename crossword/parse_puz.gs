//A very hacky way to import a crossword puzzle (.puz file) into google sheets
//Currently, META_INFO_SIZE may need to be changed to have clues show up with correct numbering

/* Things to consider:
 * - having better user input methods for modifiable variables
 * - .puz is proprietary, maybe make this work for .ipuz or others formats
 * - using less hacky parsing methods so this works on files from other sources
 * - incorporating extra features like GRBS, RTBL, LTIM, GEXT as described from
 * -   https://code.google.com/archive/p/puz/wikis/FileFormat.wiki
 * - figure out how the checksums work, there are repos on github that have implemented this
 */

//user variables
var FILE_NAME = 'sample.puz';

var OFFSET = 2; //due to implementation, OFFSET must be greater than 1
var BLANK_COLOR = '#f0f0f0'; //color of blank squares, should not be default white
var VOID_COLOR = '#333333'; //color of blacked out squares
var CLUE_WIDTH = 300; //pixel width of clue columns


//ASCII values for grid and information specific to this format
var META_INFO_SIZE = 3; //this is what it happens to be for the NYT :/

//the rest appear to be consistent
var BLANK = 45;
var VOID = 46; //black square but BLACK looks like BLANK D:
var NULL = 0;
var SIGNATURE = [65, 67, 82, 79, 83, 83, 38, 68, 79, 87, 78]; //from the third byte

var START_POS = 52; //start of grid information
var WIDTH_POS = 44;
var HEIGHT_POS = 45;
var NUM_HINTS_POS = 46;


function main() {
  
  //finds first file with title
  var files = DriveApp.getFilesByName(FILE_NAME);
  while (files.hasNext()) {
    var file = files.next();
    break;
  }

  var bytes = file.getBlob().getBytes();
  var puzzle = new PuzzleInfo(FILE_NAME, bytes[WIDTH_POS], bytes[HEIGHT_POS], bytes[NUM_HINTS_POS], bytes);

  var ss = SpreadsheetApp.create(puzzle.title + " sheet", puzzle.num_hints + OFFSET, puzzle.width + OFFSET + 3);
  var sheet = ss.getActiveSheet();
  
  init(puzzle, sheet);
  createTable(puzzle, sheet);
}

function init(puzzle, sheet) {
  var cell_size = sheet.getRowHeight(1);
  for (col = OFFSET; col < OFFSET + puzzle.width; col++) {
    sheet.setColumnWidth(col, cell_size);
  }
  var whole_range = sheet.getRange(1, 1, sheet.getMaxRows(), sheet.getMaxColumns());
  whole_range.setFontFamily('Courier New');
}

function createTable(puzzle, sheet) {
  var table_range = sheet.getRange(OFFSET, OFFSET, puzzle.height, puzzle.width);
  table_range.setHorizontalAlignment('center');
  table_range.setBorder(true, true, true, true, false, false);
  
  var clues = prepareClues(puzzle);
  var across_column = OFFSET + puzzle.width + 1;
  var down_column = OFFSET + puzzle.width + 2;
  var across_row = OFFSET;
  var down_row = OFFSET;
  sheet.setColumnWidth(across_column, CLUE_WIDTH);
  sheet.setColumnWidth(down_column, CLUE_WIDTH);

  var clue_number = 1;
  var clue_index = 0;
  var R = OFFSET + puzzle.height;
  var C = OFFSET + puzzle.width;

  for (var row = OFFSET, col = OFFSET; row < R && col < C; col++, row = (col==C)? row + 1: row, col = (col==C)? col = OFFSET: col) {
    var n = (row - OFFSET) * puzzle.height + (col - OFFSET);
    var cell = sheet.getRange(row, col);
    if (puzzle.bytes[START_POS + n] == VOID) {
      cell.setBackground(VOID_COLOR);
      cell.setFontColor(VOID_COLOR);
      cell.setValue(String.fromCharCode(VOID));
    } else {
      cell.setBackground(BLANK_COLOR);
      var is_clued = false;
      //check if cell has across clue
      var left_cell = sheet.getRange(row, col - 1);
      if (left_cell.getBackground() != BLANK_COLOR) {
        is_clued = true;
        sheet.getRange(across_row, across_column).setValue(clue_number + " " + clues[clue_index]);
        clue_index++;
        across_row++;
      }
      //check if cell has down clue
      var top_cell = sheet.getRange(row - 1, col);
      if (top_cell.getBackground() != BLANK_COLOR) {
        is_clued = true;
        sheet.getRange(down_row, down_column).setValue(clue_number + " " + clues[clue_index]);
        clue_index++;
        down_row++;
      }
      //put in a number if it has either
      if (is_clued) {
        cell.setValue(clue_number);
        clue_number++;
      }
    }
  }
}

function prepareClues(puzzle) {
  var clues = new Array(puzzle.num_hints);
  var start_index = START_POS + (puzzle.width * puzzle.height) * 2;//<< 1;
  var clue_length = 0;
  var clue_index = 0;
  for (i = start_index; i < puzzle.bytes.length; i++) {
    var byte = puzzle.bytes[i];
    if (byte == NULL) {
      if (clue_length != 0) {
        if (clue_index >= META_INFO_SIZE) {
          clues[clue_index - META_INFO_SIZE] = String.fromCharCode.apply(String, puzzle.bytes.slice(start_index, start_index + clue_length));
        }
        start_index = i + 1;
        clue_length = 0;
        clue_index++;
        if (clue_index == puzzle.num_hints + META_INFO_SIZE) {
          break;
        }
      }
    } else {
      clue_length++;
    }
  }
  return clues;
}

var PuzzleInfo = function(title, width, height, num_hints, bytes) {
  this.title = title;
  this.width = width;
  this.height = height;
  this.num_hints = num_hints;
  this.bytes = bytes;
};
