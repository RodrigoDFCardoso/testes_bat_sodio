function doGet() {
  return ContentService
    .createTextOutput("OK - Apps Script funcionando");
}


function doPost(e) {

  try {

    var dados = JSON.parse(e.postData.contents);

    var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();

    var timestamp = new Date(dados.timestamp * 1000);

    var timezone = Session.getScriptTimeZone();

    var nomeAba = Utilities.formatDate(
      timestamp,
      timezone,
      "yyyy-MM-dd"
    );

    var sheet = spreadsheet.getSheetByName(nomeAba);

    if (!sheet) {

      sheet = spreadsheet.insertSheet(nomeAba);

      sheet.appendRow([
        "Timestamp",
        "Cell A (V)",
        "Cell B (V)",
        "Cell C (V)",
        "Cell D (V)",
        "Current (A)",
        "Power (W)",
        "Temp A (°C)",
        "Temp B (°C)",
        "Temp C (°C)",
        "Temp D (°C)"
      ]);

      sheet.setFrozenRows(1);
    }

    sheet.appendRow([
      timestamp,
      dados.cell_A,
      dados.cell_B,
      dados.cell_C,
      dados.cell_D,
      dados.current,
      dados.power,
      dados.temp_A,
      dados.temp_B,
      dados.temp_C,
      dados.temp_D
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({
        status: "success",
        sheet: nomeAba
      }))
      .setMimeType(ContentService.MimeType.JSON);

  }

  catch (erro) {

    return ContentService
      .createTextOutput(JSON.stringify({
        status: "error",
        message: erro.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}