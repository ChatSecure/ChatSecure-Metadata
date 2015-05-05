#import "SnapshotHelper.js"

var target = UIATarget.localTarget();
var window = target.frontMostApp().mainWindow();
var model = target.model();

target.delay(5);

if (model.match(/iPhone/)) {
    captureLocalizedScreenshot("BuddyList");
}


function pressBackButton(target, window) {
    var navBar = window.navigationBar();
    var backButton = navBar.leftButton();
    backButton.tap();
    target.delay(1);
}

//Set correct orientation
if (model.match(/iPhone/)) {
    target.setDeviceOrientation(UIA_DEVICE_ORIENTATION_PORTRAIT);
}
else {
    target.setDeviceOrientation(UIA_DEVICE_ORIENTATION_LANDSCAPELEFT);
    target.delay(2);
}

//
// Go to messages for first buddy
//
var tableView = window.tableViews()["conversationTableView"];
tableView.cells()[0].tap();
target.delay(2);
captureLocalizedScreenshot("ChatLog");

// Go back
pressBackButton(target, window);

// Go to Setting View
var navBar = window.navigationBars()[0];
var settingsButton = navBar.rightButton();
settingsButton.tap();
target.delay(2);

//Create New Account
var tableView = window.tableViews()["settingsTableView"];
var cells = tableView.cells();
cells[1].tap();
target.delay(2);

//Select connect New Account -> Connect to Existing Account
if (model.match(/iPhone/)) {
    target.frontMostApp().actionSheet().collectionViews()[0].cells()[1].buttons()[0].tap();
}
else {
    target.frontMostApp().mainWindow().popover().actionSheet().collectionViews()[0].cells()[1].buttons()[0].tap();
}


target.delay(2);
captureLocalizedScreenshot("Accounts");

//Select XMPP Account
tableView = window.tableViews()["newAccountTableView"];
tableView.cells()[1].tap();
target.delay(1);

captureLocalizedScreenshot("XMPP_Settings");
target.delay(1);