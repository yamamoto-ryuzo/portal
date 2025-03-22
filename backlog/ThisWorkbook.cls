VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ThisWorkbook"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Option Explicit


Private Const API_KEY_NAME As String = "apiKey"
Private Const MAX_ISSUES As Long = 10
Private Const MAX_ISSUES_LIMIT As Long = 50
Private Const DATE_FORMAT As String = "yyyy/mm/dd"

' 列名の定数
Private Const COL_ID As String = "ID"
Private Const COL_PROJECT_ID As String = "プロジェクトID"
Private Const COL_ISSUE_KEY As String = "課題キー"
Private Const COL_ISSUE_TYPE_ID As String = "種別ID"
Private Const COL_ISSUE_TYPE As String = "種別"
Private Const COL_SUMMARY As String = "件名"
Private Const COL_DESCRIPTION As String = "説明"
Private Const COL_RESOLUTION As String = "解決"
Private Const COL_PRIORITY As String = "優先度"
Private Const COL_STATUS_ID As String = "状態ID"
Private Const COL_STATUS As String = "状態"
Private Const COL_ASSIGNEE As String = "担当者"
Private Const COL_CATEGORY_ID As String = "カテゴリーID"
Private Const COL_CATEGORY As String = "カテゴリー"
Private Const COL_MILESTONE_ID As String = "マイルストーンID"
Private Const COL_MILESTONE As String = "マイルストーン"
Private Const COL_START_DATE As String = "開始日"
Private Const COL_DUE_DATE As String = "期限日"
Private Const COL_ESTIMATED_HOURS As String = "予定時間"
Private Const COL_ACTUAL_HOURS As String = "実績時間"
Private Const COL_PARENT_ISSUE_ID As String = "親課題ID"
Private Const COL_CREATED_USER As String = "作成者"
Private Const COL_CREATED_DATE As String = "作成日"
Private Const COL_UPDATED_USER As String = "更新者"
Private Const COL_UPDATED_DATE As String = "更新日"
Private Const COL_CUSTOM_FIELDS As String = "カスタム属性"
Private Const COL_ATTACHMENTS As String = "添付ファイル"
Private Const COL_SHARED_FILES As String = "共有ファイル"
' カスタム属性が格納されている列の列記号
Private Const CUSTOM_COLUMNS As String = "Z"
' カスタム属性の列が開始される列番号
Private Const CUSTOM_COLUMNS_NUM As Long = 28


Sub MainProcedure()

    Call GetBacklogIssues
    Call GetBacklogCustomIssues
    
End Sub

'==============================
'===== カスタム属性を展開 =====
'==============================
Private Sub GetBacklogCustomIssues()
    Dim ws As Worksheet
    Dim lastRow As Long, lastCol As Long
    Dim i As Long, j As Long
    Dim dataArray As Variant
    Dim headers As Collection
    Dim item As Variant, attr As Variant
    Dim cellValue As String, urlValue As String
    
    Set ws = ThisWorkbook.Worksheets("issues")
    lastRow = ws.Cells(ws.Rows.Count, CUSTOM_COLUMNS).End(xlUp).row
    
    Set headers = New Collection
    
    ' すべての行からユニークな属性を抽出
    For i = 2 To lastRow
        dataArray = Split(ws.Cells(i, CUSTOM_COLUMNS).value, ", ")
        For Each item In dataArray
            attr = Split(item, ":", 2)  ' 最大2つに分割
            If UBound(attr) >= 0 Then
                On Error Resume Next
                headers.Add Trim(attr(0)), Trim(attr(0))
                On Error GoTo 0
            End If
        Next item
    Next i
    
    ' ヘッダーを設定し、背景色を薄い緑に変更
    For i = 1 To headers.Count
        ws.Cells(1, i + CUSTOM_COLUMNS_NUM).value = headers(i)
        ws.Cells(1, i + CUSTOM_COLUMNS_NUM).Interior.Color = RGB(235, 241, 222) ' 薄い緑色に設定
    Next i
    
    ' データを分解して展開
    For i = 2 To lastRow
        dataArray = Split(ws.Cells(i, CUSTOM_COLUMNS).value, ", ")
        For j = 1 To headers.Count
            ws.Cells(i, j + CUSTOM_COLUMNS_NUM).value = ""
            For Each item In dataArray
                attr = Split(item, ":", 2)  ' 最大2つに分割
                If UBound(attr) >= 0 Then
                    If Trim(attr(0)) = headers(j) Then
                        If UBound(attr) >= 1 Then
                            cellValue = Trim(attr(1))
                            ws.Cells(i, j + CUSTOM_COLUMNS_NUM).value = cellValue
                            ' セル内の文字列からURLを抽出
                            urlValue = ExtractURL(cellValue)
                            If urlValue <> "" Then
                                ' URLが見つかった場合、ハイパーリンクを設定
                                ws.Hyperlinks.Add Anchor:=ws.Cells(i, j + CUSTOM_COLUMNS_NUM), Address:=urlValue, TextToDisplay:=cellValue
                            End If
                        End If
                        Exit For
                    End If
                End If
            Next item
        Next j
    Next i
    
    MsgBox "カスタム属性の展開が完了しました。", vbInformation
End Sub

' 文字列からURLを抽出する関数
Function ExtractURL(text As String) As String
    Dim regex As Object
    Set regex = CreateObject("VBScript.RegExp")
    
    regex.Pattern = "https?://[^\s]+"
    regex.Global = False
    
    If regex.Test(text) Then
        ExtractURL = regex.Execute(text)(0)
    Else
        ExtractURL = ""
    End If
    
    Set regex = Nothing
End Function

'==========================
'===== 標準属性を展開 =====
'==========================

Private Sub GetBacklogIssues()
    On Error GoTo ErrorHandler
    
    'デバッグ　イミディエイトのクリア
    Debug.Print String(200, vbCrLf)
    
    Dim configSht As Worksheet, issueSht As Worksheet
    Dim backlogURL As String, apiKey As String, apiEndpoint As String, baseUrl As String
    Dim projectId As String, milestoneId As String, categoryId As String, statusId As String, issueTypeId As String, startDate As String, endDate As String
    Dim http As Object, response As String
    Dim issues As Collection, issueData() As Variant
    Dim i As Long, row As Long, offset As Long, totalIssues As Long
    Dim columnMap As Object
    
    Const MAX_ISSUES_PER_REQUEST As Long = 100 ' 1回のリクエストで取得する最大課題数
    Dim MAX_TOTAL_ISSUES As Long ' 取得する課題の最大数
    
    ' 設定シートからBacklogのURLとAPIキーを取得
    Set configSht = ThisWorkbook.Worksheets("config")
    backlogURL = configSht.Range("B1").value
    apiKey = configSht.Range("B2").value
    projectId = configSht.Range("B3").value
    milestoneId = configSht.Range("B4").value
    categoryId = configSht.Range("B5").value
    statusId = configSht.Range("B6").value
    MAX_TOTAL_ISSUES = configSht.Range("B7").value ' 新しい設定：取得する課題の最大数
    issueTypeId = configSht.Range("B8").value ' B8から種別IDを取得
    startDate = configSht.Range("B9").value ' B9から期限日取得開始日を取得
    endDate = configSht.Range("B10").value ' B10から期限日取得最終日を取得
    
    apiEndpoint = "api/v2/issues?"
    
    ' ベースURLの構築
    baseUrl = backlogURL & apiEndpoint & "apiKey=" & apiKey & "&count=" & MAX_ISSUES_PER_REQUEST
    
    ' オプションパラメータの追加
    If Len(projectId) > 0 Then baseUrl = baseUrl & "&projectId[]=" & WorksheetFunction.EncodeURL(projectId)
    If Len(milestoneId) > 0 Then baseUrl = baseUrl & "&milestoneId[]=" & WorksheetFunction.EncodeURL(milestoneId)
    If Len(categoryId) > 0 Then baseUrl = baseUrl & "&categoryId[]=" & WorksheetFunction.EncodeURL(categoryId)
    If Len(statusId) > 0 Then baseUrl = baseUrl & "&statusId[]=" & WorksheetFunction.EncodeURL(statusId)
    If Len(issueTypeId) > 0 Then baseUrl = baseUrl & "&issueTypeId[]=" & WorksheetFunction.EncodeURL(issueTypeId) ' 種別IDを追加
    If Len(startDate) > 0 Then baseUrl = baseUrl & "&dueDateSince=" & WorksheetFunction.EncodeURL(startDate) ' 期限日検索開始日を追加
    If Len(endDate) > 0 Then baseUrl = baseUrl & "&dueDateUntil=" & WorksheetFunction.EncodeURL(endDate) ' 期限日検索最終日を追加
    Debug.Print "======================== ベースURL　========================"
    Debug.Print baseUrl
    
    ' 課題一覧を表示するシートの準備
    Set issueSht = ThisWorkbook.Worksheets("issues")
    issueSht.Cells.Clear
    
    ' ヘッダー行の設定と列マップの作成
    Set columnMap = SetHeaders(issueSht)
    
    Set issues = New Collection
    offset = 0
    
    Do
        ' APIリクエストURLの構築（OFFSETを含む）
        Dim url As String
        url = baseUrl & "&offset=" & offset
        
        ' HTTPリクエストの準備と送信
        Set http = CreateObject("MSXML2.XMLHTTP")
        http.Open "GET", url, False
        http.Send
        
        ' APIレスポンスの処理
        If http.Status = 200 Then
            response = http.responseText
            Debug.Print "==========================http.responseTextレスポンスの表示=========================="
            Debug.Print http.responseText
            
            ' レスポンスを個別の課題データに分割し、Collectionに追加
            Dim tempIssues() As String
            tempIssues = Split(response, "]},{")
            
            For i = 0 To UBound(tempIssues)
                issues.Add tempIssues(i)
                If issues.Count >= MAX_TOTAL_ISSUES Then
                    Exit For
                End If
            Next i
            
            ' 次のオフセットを設定
            offset = offset + MAX_ISSUES_PER_REQUEST
            
            ' 取得した課題数が100未満なら終了、または最大課題数に達したら終了
            If UBound(tempIssues) + 1 < MAX_ISSUES_PER_REQUEST Or issues.Count >= MAX_TOTAL_ISSUES Then
                Exit Do
            End If
        Else
            Err.Raise vbObjectError + 1, , "APIエラー: ステータスコード " & http.Status
        End If
    Loop
    
    ' 全ての課題データを処理
    ReDim issueData(1 To issues.Count, 1 To columnMap.Count)
    For i = 1 To issues.Count
        ProcessIssue issues(i), issueData, i, columnMap
        Debug.Print "=====メッセージにて課題を表示====="
        Debug.Print issues(i)
    Next i
    
    ' データをシートに書き込み
    WriteDataToSheet issueSht, issueData
    
    ' 列幅の自動調整
    ' issueSht.UsedRange.Columns.AutoFit
    
    MsgBox "課題一覧を取得しました。合計 " & issues.Count & " 件の課題が見つかりました。", vbInformation
    
    Exit Sub

ErrorHandler:
    MsgBox "エラーが発生しました: " & Err.Description, vbCritical
End Sub


'==================================
'===== エクセルに表示する属性 =====
'==================================

Private Function SetHeaders(sht As Worksheet) As Object
    Dim columnMap As Object
    Dim headers() As Variant
    Dim i As Long, col As Long
    Set columnMap = CreateObject("Scripting.Dictionary")
    
    '==================
    '表示する配列の実態
    '==================
    headers = Array( _
        COL_ID, COL_PROJECT_ID, COL_ISSUE_KEY, COL_ISSUE_TYPE_ID, COL_ISSUE_TYPE, COL_SUMMARY, _
        COL_DESCRIPTION, COL_RESOLUTION, COL_PRIORITY, COL_STATUS_ID, COL_STATUS, COL_ASSIGNEE, _
        COL_CATEGORY_ID, COL_CATEGORY, COL_MILESTONE_ID, COL_MILESTONE, COL_START_DATE, COL_DUE_DATE, _
        COL_ESTIMATED_HOURS, COL_ACTUAL_HOURS, COL_PARENT_ISSUE_ID, _
        COL_CREATED_USER, COL_CREATED_DATE, COL_UPDATED_USER, COL_UPDATED_DATE, _
        COL_CUSTOM_FIELDS, COL_ATTACHMENTS, COL_SHARED_FILES _
    )
    
    'ヘッダーの設定とマッピング
    col = 1
    For i = LBound(headers) To UBound(headers)
        If Len(headers(i)) > 0 Then
            sht.Cells(1, col).value = headers(i)
            columnMap.Add headers(i), col
            col = col + 1
        End If
    Next i
    
    'ヘッダー行の書式設定
    With sht.Range(sht.Cells(1, 1), sht.Cells(1, col - 1))
        .Font.Bold = True
        .Interior.Color = RGB(220, 230, 241)  ' 薄い青色
        .HorizontalAlignment = xlCenter
    End With
    
    'オートフィルターの適用
    sht.Range(sht.Cells(1, 1), sht.Cells(1, col - 1)).AutoFilter
    
    Set SetHeaders = columnMap
End Function

Private Sub ProcessIssue(issue As String, ByRef data() As Variant, row As Long, columnMap As Object)
    If columnMap.Exists(COL_ID) Then data(row, columnMap(COL_ID)) = ExtractValue(issue, "id")
    If columnMap.Exists(COL_PROJECT_ID) Then data(row, columnMap(COL_PROJECT_ID)) = ExtractValue(issue, "projectId")
    If columnMap.Exists(COL_ISSUE_KEY) Then data(row, columnMap(COL_ISSUE_KEY)) = ExtractValue(issue, "issueKey")
    If columnMap.Exists(COL_ISSUE_TYPE_ID) Then data(row, columnMap(COL_ISSUE_TYPE_ID)) = ExtractNestedValue(issue, "issueType", "id")
    If columnMap.Exists(COL_ISSUE_TYPE) Then data(row, columnMap(COL_ISSUE_TYPE)) = ExtractNestedValue(issue, "issueType", "name")
    If columnMap.Exists(COL_SUMMARY) Then data(row, columnMap(COL_SUMMARY)) = ExtractValue(issue, "summary")
    If columnMap.Exists(COL_DESCRIPTION) Then data(row, columnMap(COL_DESCRIPTION)) = ExtractValue(issue, "description")
    If columnMap.Exists(COL_RESOLUTION) Then data(row, columnMap(COL_RESOLUTION)) = ExtractValue(issue, "resolution")
    If columnMap.Exists(COL_PRIORITY) Then data(row, columnMap(COL_PRIORITY)) = ExtractNestedValue(issue, "priority", "name")
    If columnMap.Exists(COL_STATUS_ID) Then data(row, columnMap(COL_STATUS_ID)) = ExtractNestedValue(issue, "status", "id")
    If columnMap.Exists(COL_STATUS) Then data(row, columnMap(COL_STATUS)) = ExtractNestedValue(issue, "status", "name")
    If columnMap.Exists(COL_ASSIGNEE) Then data(row, columnMap(COL_ASSIGNEE)) = ExtractNestedValue(issue, "assignee", "name")
    If columnMap.Exists(COL_CATEGORY_ID) Then data(row, columnMap(COL_CATEGORY_ID)) = ExtractArrayValues(issue, "category", "id")
    If columnMap.Exists(COL_CATEGORY) Then data(row, columnMap(COL_CATEGORY)) = ExtractArrayValues(issue, "category", "name")
    If columnMap.Exists(COL_MILESTONE_ID) Then data(row, columnMap(COL_MILESTONE_ID)) = ExtractArrayValues(issue, "milestone", "id")
    If columnMap.Exists(COL_MILESTONE) Then data(row, columnMap(COL_MILESTONE)) = ExtractArrayValues(issue, "milestone", "name")
    If columnMap.Exists(COL_START_DATE) Then data(row, columnMap(COL_START_DATE)) = ConvertDateFormat(ExtractValue(issue, "startDate"))
    If columnMap.Exists(COL_DUE_DATE) Then data(row, columnMap(COL_DUE_DATE)) = ConvertDateFormat(ExtractValue(issue, "dueDate"))
    If columnMap.Exists(COL_ESTIMATED_HOURS) Then data(row, columnMap(COL_ESTIMATED_HOURS)) = ExtractValue(issue, "estimatedHours")
    If columnMap.Exists(COL_ACTUAL_HOURS) Then data(row, columnMap(COL_ACTUAL_HOURS)) = ExtractValue(issue, "actualHours")
    If columnMap.Exists(COL_PARENT_ISSUE_ID) Then data(row, columnMap(COL_PARENT_ISSUE_ID)) = ExtractValue(issue, "parentIssueId")
    If columnMap.Exists(COL_CREATED_USER) Then data(row, columnMap(COL_CREATED_USER)) = ExtractNestedValue(issue, "createdUser", "name")
    If columnMap.Exists(COL_CREATED_DATE) Then data(row, columnMap(COL_CREATED_DATE)) = ConvertDateFormat(ExtractValue(issue, "created"))
    If columnMap.Exists(COL_UPDATED_USER) Then data(row, columnMap(COL_UPDATED_USER)) = ExtractNestedValue(issue, "updatedUser", "name")
    If columnMap.Exists(COL_UPDATED_DATE) Then data(row, columnMap(COL_UPDATED_DATE)) = ConvertDateFormat(ExtractValue(issue, "updated"))
    If columnMap.Exists(COL_CUSTOM_FIELDS) Then data(row, columnMap(COL_CUSTOM_FIELDS)) = ExtractCustomFields(issue)
    If columnMap.Exists(COL_ATTACHMENTS) Then data(row, columnMap(COL_ATTACHMENTS)) = ExtractArrayValues(issue, "attachments", "name")
    If columnMap.Exists(COL_SHARED_FILES) Then data(row, columnMap(COL_SHARED_FILES)) = ExtractArrayValues(issue, "sharedFiles", "name")
End Sub



Function ExtractArrayValues(jsonString As String, arrayName As String, fieldName As String) As String
    Dim regex As Object
    Dim matches As Object
    Dim match As Object
    Dim result As String
    
    Set regex = CreateObject("VBScript.RegExp")
    regex.Global = True
    regex.Pattern = """" & arrayName & """:\s*\[(.*?)\]"
    
    Set matches = regex.Execute(jsonString)
    
    If matches.Count > 0 Then
        Dim arrayContent As String
        arrayContent = matches(0).SubMatches(0)
        
        regex.Pattern = "{(.*?)}"
        Set matches = regex.Execute(arrayContent)
        
        For Each match In matches
            Dim itemContent As String
            itemContent = match.SubMatches(0)
            
            Dim fieldRegex As Object
            Set fieldRegex = CreateObject("VBScript.RegExp")
            fieldRegex.Global = False
            fieldRegex.Pattern = """" & Trim(fieldName) & """\s*:\s*(""[^""]*""|[^,}\s]+)"
            
            Dim fieldMatch As Object
            Set fieldMatch = fieldRegex.Execute(itemContent)
            
            If fieldMatch.Count > 0 Then
                If Len(result) > 0 Then result = result & ","
                result = result & fieldMatch(0).SubMatches(0)
            End If
        Next match
    End If
    
    ' 文字列の場合、前後の引用符を削除
    If Left(result, 1) = """" And Right(result, 1) = """" Then
        result = Mid(result, 2, Len(result) - 2)
    End If
    
    ExtractArrayValues = result
End Function




Function ExtractCustomFields(jsonString As String) As String
    Dim regex As Object
    Dim matches As Object
    Dim match As Object
    Dim result As String
    
    Set regex = CreateObject("VBScript.RegExp")
    regex.Global = True
    regex.Pattern = """customFields"":\s*(\[.*?\])"
    
    Set matches = regex.Execute(jsonString)
    
    If matches.Count > 0 Then
        Dim customFieldsJson As String
        customFieldsJson = matches(0).SubMatches(0)
        
        ' カスタムフィールドのパターンを修正
        regex.Pattern = "{""id"":(\d+),""fieldTypeId"":\d+,""name"":""([^""]*)"",""value"":([^}]*)}"
        Set matches = regex.Execute(customFieldsJson)
        
        For Each match In matches
            Dim fieldName As String, fieldValue As String
            fieldName = match.SubMatches(1)
            fieldValue = match.SubMatches(2)
            
            ' fieldValueがオブジェクトの場合の処理を追加
            If Left(Trim(fieldValue), 1) = "{" Then
                fieldValue = ExtractValue(fieldValue, "name") ' オブジェクトからnameを抽出
            Else
                ' valueがnullの場合は空文字列に置き換える
                If LCase(fieldValue) = "null" Then
                    fieldValue = ""
                Else
                    ' 最初と最後のダブルクォーテーションを削除
                    If Left(fieldValue, 1) = """" And Right(fieldValue, 1) = """" Then
                        fieldValue = Mid(fieldValue, 2, Len(fieldValue) - 2)
                    End If
                End If
            End If
            
            If Len(result) > 0 Then result = result & ", "
            result = result & fieldName & ": " & fieldValue
        Next match
    End If
    
    ExtractCustomFields = result
End Function



Private Sub WriteDataToSheet(sht As Worksheet, data() As Variant)
    Dim i As Long, j As Long
    
    For i = LBound(data) To UBound(data)
        For j = LBound(data, 2) To UBound(data, 2)
            If VarType(data(i, j)) = vbString Then
                data(i, j) = Replace(data(i, j), "\n", Chr(10))
            End If
        Next j
    Next i
    
    sht.Range("A2").Resize(UBound(data), UBound(data, 2)).value = data
End Sub


Function ExtractNestedValue(jsonString As String, parentKey As String, childKey As String) As String
    Dim regex As Object
    Dim matches As Object
    
    Set regex = CreateObject("VBScript.RegExp")
    regex.Global = True
    regex.Pattern = """" & parentKey & """\s*:\s*\{[^\}]*""" & childKey & """\s*:\s*([^,\}]+)"
    
    Set matches = regex.Execute(jsonString)
    
    If matches.Count > 0 Then
        Dim value As String
        value = Trim(matches(0).SubMatches(0))
        
        ' 引用符がある場合は削除し、ない場合はそのまま文字列として返す
        If Left(value, 1) = """" And Right(value, 1) = """" Then
            ExtractNestedValue = Mid(value, 2, Len(value) - 2)
        Else
            ExtractNestedValue = value
        End If
    Else
        ExtractNestedValue = ""
    End If
End Function





Private Function ExtractValue(jsonString As String, key As String) As String
    Dim pos As Long, endPos As Long, nestLevel As Integer
    Dim value As String, char As String
    
    pos = InStr(1, jsonString, """" & key & """:")
    If pos > 0 Then
        pos = pos + Len(key) + 3
        Select Case Mid(jsonString, pos, 1)
            Case """"  ' 文字列値
                pos = pos + 1
                endPos = InStr(pos, jsonString, """")
                While Mid(jsonString, endPos - 1, 1) = "\"
                    endPos = InStr(endPos + 1, jsonString, """")
                Wend
                value = Mid(jsonString, pos, endPos - pos)
            Case "{", "["  ' オブジェクトまたは配列
                nestLevel = 1
                endPos = pos
                Do
                    endPos = endPos + 1
                    char = Mid(jsonString, endPos, 1)
                    Select Case char
                        Case "{", "[": nestLevel = nestLevel + 1
                        Case "}", "]": nestLevel = nestLevel - 1
                    End Select
                Loop Until nestLevel = 0
                value = Mid(jsonString, pos, endPos - pos + 1)
            Case Else  ' 数値や真偽値
                endPos = InStr(pos, jsonString, ",")
                If endPos = 0 Then endPos = InStr(pos, jsonString, "}")
                If endPos = 0 Then endPos = Len(jsonString) + 1
                value = Trim(Mid(jsonString, pos, endPos - pos))
        End Select
        
        ' 数値の場合、ダブルクォートを削除
        If IsNumeric(value) Then
            value = Replace(value, """", "")
        End If
        
        ExtractValue = value
    End If
End Function

Function ParseSimpleJson(jsonString As String) As Object
    Dim dict As Object
    Set dict = CreateObject("Scripting.Dictionary")
    
    jsonString = Mid(jsonString, 2, Len(jsonString) - 2)  ' 最初と最後の { } を削除
    Dim pairs() As String
    pairs = Split(jsonString, ",")
    
    Dim i As Long
    For i = 0 To UBound(pairs)
        Dim keyValue() As String
        keyValue = Split(pairs(i), ":")
        Dim key As String, value As String
        key = Trim(Replace(keyValue(0), """", ""))
        value = Trim(Replace(keyValue(1), """", ""))
        dict.Add key, value
    Next i
    
    Set ParseSimpleJson = dict
End Function


Private Function ConvertDateFormat(dateStr As String) As String
    If Len(dateStr) >= 10 Then
        Dim year As String, month As String, day As String
        year = Mid(dateStr, 1, 4)
        month = Mid(dateStr, 6, 2)
        day = Mid(dateStr, 9, 2)
        ConvertDateFormat = year & "/" & month & "/" & day
    Else
        ConvertDateFormat = dateStr
    End If
End Function



