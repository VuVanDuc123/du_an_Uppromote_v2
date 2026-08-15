// Copy toàn bộ file này vào Google Sheets > Tiện ích mở rộng > Apps Script (ghi đè code cũ)
// Sau đó: Triển khai > Quản lý các bản triển khai > bấm biểu tượng bút chì (Edit) trên bản đang có
// > Phiên bản (Version): chọn "Phiên bản mới" (New version) > Triển khai (Deploy)
// (Giữ nguyên URL cũ, không cần tạo bản triển khai mới)
//
// Cột trong sheet "Status": A=id, B=status, C=updated_at, D=test_result, E=test_note

function doGet(e) {
  const sheet = getStatusSheet();
  const data = sheet.getDataRange().getValues();
  const result = {};
  for (let i = 1; i < data.length; i++) {
    const id = data[i][0];
    if (id === '') continue;
    const entry = {};
    if (data[i][1] !== '') entry.status = data[i][1];
    if (data[i][3] !== '') entry.test_result = data[i][3];
    if (data[i][4] !== '') entry.test_note = data[i][4];
    result[id] = entry;
  }
  return ContentService.createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  const sheet = getStatusSheet();
  const params = JSON.parse(e.postData.contents);
  const id = params.id;

  const data = sheet.getDataRange().getValues();
  let rowIndex = -1;
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] == id) {
      rowIndex = i + 1;
      break;
    }
  }
  if (rowIndex === -1) {
    rowIndex = sheet.getLastRow() + 1;
    sheet.getRange(rowIndex, 1).setValue(id);
  }

  if (params.status !== undefined) sheet.getRange(rowIndex, 2).setValue(params.status);
  if (params.test_result !== undefined) sheet.getRange(rowIndex, 4).setValue(params.test_result);
  if (params.test_note !== undefined) sheet.getRange(rowIndex, 5).setValue(params.test_note);
  sheet.getRange(rowIndex, 3).setValue(new Date());

  return ContentService.createTextOutput(JSON.stringify({ success: true }))
    .setMimeType(ContentService.MimeType.JSON);
}

function getStatusSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName('Status');
  if (!sheet) {
    sheet = ss.insertSheet('Status');
    sheet.appendRow(['id', 'status', 'updated_at', 'test_result', 'test_note']);
  }
  return sheet;
}
