// Copy toàn bộ file này vào Google Sheets > Tiện ích mở rộng > Apps Script
// Sau đó bấm Triển khai (Deploy) > Ứng dụng web (Web app) để lấy URL API.

function doGet(e) {
  const sheet = getStatusSheet();
  const data = sheet.getDataRange().getValues();
  const result = {};
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] !== '') result[data[i][0]] = data[i][1];
  }
  return ContentService.createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  const sheet = getStatusSheet();
  const params = JSON.parse(e.postData.contents);
  const id = params.id;
  const status = params.status;

  const data = sheet.getDataRange().getValues();
  let found = false;
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] == id) {
      sheet.getRange(i + 1, 2).setValue(status);
      sheet.getRange(i + 1, 3).setValue(new Date());
      found = true;
      break;
    }
  }
  if (!found) {
    sheet.appendRow([id, status, new Date()]);
  }

  return ContentService.createTextOutput(JSON.stringify({ success: true }))
    .setMimeType(ContentService.MimeType.JSON);
}

function getStatusSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName('Status');
  if (!sheet) {
    sheet = ss.insertSheet('Status');
    sheet.appendRow(['id', 'status', 'updated_at']);
  }
  return sheet;
}