var ss = SpreadsheetApp.getActiveSpreadsheet();

var RANGE_COMMANDERS = 'FirstCommander';

var SHEET_COMMANDERS = 'Commanders';

function onOpen() {
  ss.addMenu('Generate Brackets',
    [
      {name: 'Generate Small Bracket', functionName: 'createSmallBracket'}, 
      {name: 'Generate Medium Bracket', functionName: 'createMediumBracket'}, 
      {name: 'Generate Large Bracket', functionName: 'createLargeBracket'}
    ]
  );
}

function createSmallBracket() {
  createBracket('small');
}

function createMediumBracket() {
  createBracket('medium');
}

function createLargeBracket() {
  createBracket('large');
}

// "all" keyword can be considered, but it would honestly be better to generate the brackets one at a time.


function createBracket(size) {
  // eg. SHEET_DETERMINED_BRACKET_SIZE = 'Small Bracket'
  // countNodesUpperBound later on will be used to determine the bracket size, and is just an int (32, 16, 8, or 4)
  // Combining SHEET_DETERMINED_BRACKET_SIZE with countNodesUpperBound later on will get us with something like
  // var sheet = "Small Bracket 32", which is how we can generically link these display variables to an existing sheet.

  // Is it messy? Probably. If I had more time to dedicate to google scripts I'd probably make it better,
  // but this serves its function and doesn't have many nasty drawbacks.
  var RANGE_SHIPS;
  var SHEET_DETERMINED_BRACKET_SIZE;
  var DISPLAY_BRACKET_SIZE_32;
  var DISPLAY_BRACKET_SIZE_16;
  var DISPLAY_BRACKET_SIZE_8;
  var DISPLAY_BRACKET_SIZE_4;

  var displayBracketSize32;
  var displayBracketSize16;
  var displayBracketSize8;
  var displayBracketSize4;

  if (size == 'small') {
    DISPLAY_BRACKET_SIZE_32 = 'Small Bracket 32';
    DISPLAY_BRACKET_SIZE_16 = 'Small Bracket 16';
    DISPLAY_BRACKET_SIZE_8  = 'Small Bracket 8';
    DISPLAY_BRACKET_SIZE_4  = 'Small Bracket 4';
    RANGE_SHIPS = 'FirstSmallShip';
    SHEET_DETERMINED_BRACKET_SIZE = 'Small Bracket';
  } 
  else if (size == 'medium') {
    DISPLAY_BRACKET_SIZE_32 = 'Medium Bracket 32';
    DISPLAY_BRACKET_SIZE_16 = 'Medium Bracket 16';
    DISPLAY_BRACKET_SIZE_8  = 'Medium Bracket 8';
    DISPLAY_BRACKET_SIZE_4  = 'Medium Bracket 4';
    RANGE_SHIPS = 'FirstMediumShip';
    SHEET_DETERMINED_BRACKET_SIZE = 'Medium Bracket';
  } 
  else if (size == 'large') {
    DISPLAY_BRACKET_SIZE_32 = 'Large Bracket 32';
    DISPLAY_BRACKET_SIZE_16 = 'Large Bracket 16';
    DISPLAY_BRACKET_SIZE_8  = 'Large Bracket 8';
    DISPLAY_BRACKET_SIZE_4  = 'Large Bracket 4';
    RANGE_SHIPS = 'FirstLargeShip';
    SHEET_DETERMINED_BRACKET_SIZE = 'Large Bracket';
  } 
  else {
    return;
  }

  displayBracketSize32 = ss.getSheetByName(DISPLAY_BRACKET_SIZE_32);
  displayBracketSize16 = ss.getSheetByName(DISPLAY_BRACKET_SIZE_16);
  displayBracketSize8 = ss.getSheetByName(DISPLAY_BRACKET_SIZE_8);
  displayBracketSize4 = ss.getSheetByName(DISPLAY_BRACKET_SIZE_4);

  var rangeCommanders = ss.getRangeByName(RANGE_COMMANDERS);
  var rangeShips = ss.getRangeByName(RANGE_SHIPS)
  var sheetCommanders = ss.getSheetByName(SHEET_COMMANDERS);

  rangeCommanders = rangeCommanders.offset(0, 0, sheetCommanders.getMaxRows() -
      rangeCommanders.getRowIndex() + 1, 1);
  rangeShips = rangeShips.offset(0, 0, sheetCommanders.getMaxRows() -
      rangeShips.getRowIndex() + 1, 1);
  var commanders = rangeCommanders.getValues();
  var sizeShips = rangeShips.getValues();
  
  // Now figure out how many commanders there are.
  var numCommanders = 0;
  for (var i = 0; i < commanders.length; i++) {
    if (!commanders[i][0] || commanders[i][0].length == 0) {
      if (!commanders[i + 1][0]) {
        break
      }
      // continue;
      // break;
    }
    numCommanders++;
  }
  commanders = commanders.slice(0, numCommanders);
  sizeShips = sizeShips.slice(0, numCommanders);

  var filteredCommanders = [];
  for (var i = 0; i < commanders.length; i++) {
    if (sizeShips[i][0]) {
      filteredCommanders.push(commanders[i]);
    } continue;
  }

  var filteredNumCommanders = filteredCommanders.length;

  // Provide some error checking in case there are too many or too few players/teams.
  if (filteredNumCommanders > 64) {
    Browser.msgBox('Sorry, this script can only create brackets for 64 or fewer Commanders.');
    return;
  }

  if (filteredNumCommanders < 3) {
    Browser.msgBox('Sorry, you must have at least 3 Commanders in this bracket for automatic generation.');
    return;
  }

  var upperPower = Math.ceil(Math.log(filteredNumCommanders) / Math.log(2));

  // Find out what is the number that is a power of 2 and lower than numCommanders.
  var countNodesUpperBound = Math.pow(2, upperPower);

  // Find out what is the number that is a power of 2 and higher than numCommanders.
  var countNodesLowerBound = countNodesUpperBound / 2;

  // This is the number of nodes that will not show in the 1st level.
  var countNodesHidden = filteredNumCommanders - countNodesLowerBound;

  // Determine & show only the sheet that matters for this generation based on the upperBound
  var sheetDeterminedBracket = ss.getSheetByName(SHEET_DETERMINED_BRACKET_SIZE + " " + countNodesUpperBound);

  if (sheetDeterminedBracket.isSheetHidden() == false) {
    var ui = SpreadsheetApp.getUi();
    var result = ui.alert(
      'Please confirm',
      'A sheet in this bracket has already been generated and is not hidden, proceed with generating a new bracket?',
    ui.ButtonSet.YES_NO);
    if (result == ui.Button.YES) {
      ui.alert('Generating a new bracket.');
    } else {
    return;
    }
  }

  // Hide all sheets of this size
  displayBracketSize32.hideSheet();
  displayBracketSize16.hideSheet();
  displayBracketSize8.hideSheet();
  displayBracketSize4.hideSheet();

  sheetDeterminedBracket.showSheet();

  // Clear content based on display type, anything less than 32 only have values in C2:C
  // 32+ will have layer 1 values in C2:C & AI2:AI
  // Additionally, uncheck all of the boxes in both > and < 32 upperBound values
  if (countNodesUpperBound <= 16) {
    var rangedList;
    if (countNodesUpperBound == 4) {
      rangedList = sheetDeterminedBracket.getRangeList(
        ['B3:B8', 'F5:F6']
      );
      rangedList.uncheck();
    } else if (countNodesUpperBound == 8) {
      rangedList = sheetDeterminedBracket.getRangeList(
        ['B3:B15', 'F5:F14', 'J9:J10']
      );
      rangedList.uncheck();
    } else if (countNodesUpperBound == 16) {
      rangedList = sheetDeterminedBracket.getRangeList(
        ['B3:B32', 'F5:F30', 'J9:J26', 'N17:N18']
      );
      rangedList.uncheck();
    }
    var contentRange = sheetDeterminedBracket.getRange('C2:C' + ((countNodesUpperBound * 2) + 1));
    contentRange.clearContent();
  }
  if (countNodesUpperBound >= 32) {
    var rangedList = sheetDeterminedBracket.getRangeList(
      ['B3:B32', 'F5:F30', 'J9:J26', 'N17:V18', 'Z9:Z26', 'AD5:AD30', 'AH3:AH32']
    );
    rangedList.uncheck();
    var contentRange32 = sheetDeterminedBracket.getRange('C2:C' + ((countNodesUpperBound) + 1));
    var contentRangeExtended = sheetDeterminedBracket.getRange('AI2:AI' + ((countNodesUpperBound) + 1));
    contentRange32.clearContent();
    contentRangeExtended.clearContent();
  }

  // Enter the commanders for the 1st round
  var c = 0;
  if (countNodesUpperBound >= 32) {
    for (var i = 0; i < countNodesLowerBound; i++) {
      if (i < (countNodesLowerBound / 2)) {
        // Must be on the first level
        var rng = sheetDeterminedBracket.getRange(i * 4 + 3, 3);
        setBracketItem_(rng, filteredCommanders);
        setBracketItem_(rng.offset(1, 0, 1, 1), filteredCommanders);
        setBracketItem_(rng.offset(1, 2, 1, 1));
      } 
      else if (i < countNodesLowerBound) {
        // Must be on the first level
        var rng = sheetDeterminedBracket.getRange(c * 4 + 3, 35);
        setBracketItem_(rng, filteredCommanders);
        setBracketItem_(rng.offset(1, 0, 1, 1), filteredCommanders);
        setBracketItem_(rng.offset(1, 2, 1, 1));
        c++;
      } 
      else {
        setBracketItem_(sheetDeterminedBracket.getRange(i * 4 + 3, 3), filteredCommanders)
      }
    }
    upperPower--;
    for (var i = 0; i < upperPower; i++) {
      var pow1 = Math.pow(2, i + 2);
      var pow2 = Math.pow(2, i + 3);
      for (var j = 0; j < Math.pow(2, upperPower - i - 1); j++) {
        setBracketItem_(sheetDeterminedBracket.getRange((j * pow2) + pow1, i * 2 + 5));
      }
    }
  }
  if (countNodesUpperBound < 32) {
    for (var i = 0; i < countNodesLowerBound; i++) {
      if (i < (countNodesHidden)) {
        // Must be on the first level
        var rng = sheetDeterminedBracket.getRange(i * 4 + 3, 3);
        setBracketItem_(rng, filteredCommanders);
        setBracketItem_(rng.offset(1, 0, 1, 1), filteredCommanders);
        setBracketItem_(rng.offset(1, 2, 1, 1));
      } else {
          setBracketItem_(sheetDeterminedBracket.getRange(i * 4 + 3, 3), filteredCommanders)
        }
    }
    upperPower--;
    for (var i = 0; i < upperPower; i++) {
      var pow1 = Math.pow(2, i + 2);
      var pow2 = Math.pow(2, i + 3);
      for (var j = 0; j < Math.pow(2, upperPower - i - 1); j++) {
        setBracketItem_(sheetDeterminedBracket.getRange((j * pow2) + pow1, i * 2 + 5));
      }
    }
  }
}

function wipeCheckmarks() {
  var sheet = ss.getActiveSheet()
  var range = ('Layer1Checkmarks');
  sheet.getRange(range).uncheck();
}

function setBracketItem_(rng, commanders) {
  if (commanders) {
    var rand = Math.ceil(Math.random() * commanders.length);
    if (commanders.length == 0) {
      return;
    }
    rng.setValue(commanders.splice(rand - 1, 1)[0][0]);
  }
}




