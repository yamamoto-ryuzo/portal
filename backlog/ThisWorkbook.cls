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
Private Const MAX_ISSUES As Long = 100
Private Const DATE_FORMAT As String = "yyyy/mm/dd"

' 列名の定数
Private Const COL_ID As String = "ID"
Private Const COL_projectId As String = "プロジェクトID"
Private Const COL_ISSUE_KEY As String = "課題キー"
Private Const COL_issueType As String = "種別"
Private Const COL_SUMMARY As String = "件名"
Private Const COL_description As String = "説明"
Private Const COL_STATUS As String = "状態"
Private Const COL_ASSIGNEE As String = "担当者"
Private Const COL_START_DATE As String = "開始日"
Private Const COL_DUE_DATE As String = "期限日"
Private Const COL_customFields As String = "カスタム属性"
'headers = Array( COL_ID,COL_ISSUE_KEY,COL_issueType, COL_SUMMARY,COL_description, COL_STATUS, COL_ASSIGNEE, COL_START_DATE, COL_DUE_DATE, COL_customFields)

Sub MainProcedure()

    Call GetBacklogIssues
    Call ProcessJsonData
    
End Sub

'===================================================

Private Sub ProcessJsonData()
    Dim ws As Worksheet
    Dim jsonText As String
    Dim row As Long, col As Long, lastRow As Long
    Dim headers As Object
    Dim regEx As Object
    Dim matches As Object
    Dim match As Object
    Dim name As String, value As String
    Dim cell As Range
    
    Set ws = ThisWorkbook.Worksheets("issues")
    Set headers = CreateObject("Scripting.Dictionary")
    Set regEx = CreateObject("VBScript.RegExp")
    
    ' G列の最後の行を取得
    lastRow = ws.Cells(ws.Rows.Count, "J").End(xlUp).row
    
    ' JSONデータが格納されているセルの範囲を指定
    Dim jsonRange As Range
    Set jsonRange = ws.Range("J2:J" & lastRow)
    
    row = 2 ' 結果を書き込み始める行
    col = 11 ' 結果を書き込み始める列（K列）
    
    ' 正規表現パターンの設定
    regEx.Global = True
    regEx.Pattern = """name"":""([^""]+)"",""value"":([^,}\]]+)"
    
    ' JSONデータを処理
    For Each cell In jsonRange
        jsonText = cell.value
        Set matches = regEx.Execute(jsonText)
        
        For Each match In matches
            name = match.SubMatches(0)
            value = match.SubMatches(1)
            
            ' valueがnullの場合は空文字列に置き換える
            If value = "null" Then
                value = ""
            Else
                ' 最初と最後のダブルクォーテーションを削除
                If Left(value, 1) = """" And Right(value, 1) = """" Then
                    value = Mid(value, 2, Len(value) - 2)
                End If
                
                ' \nをエクセルの改行コードに置換
                value = Replace(value, "\n", Chr(10))
            End If
            
            ' ヘッダーが存在しない場合は新しい列を作成
            If Not headers.Exists(name) Then
                headers(name) = col
                ws.Cells(1, col).value = name
                col = col + 1
            End If
            
            ' valueの値を書き込む
            ws.Cells(row, headers(name)).value = value
        Next match
        
        row = row + 1
    Next cell
    
    ' 特殊なケース（オブジェクト値）の処理
    ProcessSpecialCases ws, jsonRange, headers
End Sub

Sub ProcessSpecialCases(ws As Worksheet, jsonRange As Range, headers As Object)
    Dim regEx As Object
    Dim matches As Object
    Dim match As Object
    Dim row As Long
    Dim cell As Range
    
    Set regEx = CreateObject("VBScript.RegExp")
    regEx.Global = True
    regEx.Pattern = """name"":""(工務課|ＰＰＰ)"",""value"":\{""id"":\d+,""name"":""([^""]+)"""
    
    row = 2
    For Each cell In jsonRange
        Set matches = regEx.Execute(cell.value)
        For Each match In matches
            ws.Cells(row, headers(match.SubMatches(0))).value = match.SubMatches(1)
        Next match
        row = row + 1
    Next cell
End Sub





'==============================================================================================


Private Sub GetBacklogIssues()
    On Error GoTo ErrorHandler
    
    'デバッグ　イミディエイトのクリア
    Debug.Print String(200, vbCrLf)
    
    Dim configSht As Worksheet, issueSht As Worksheet
    Dim backlogURL As String, apiKey As String, apiEndpoint As String, url As String
    Dim projectId As String, milestoneId As String
    Dim http As Object, response As String
    Dim issues() As String, issueData() As Variant
    Dim i As Long, row As Long
    Dim columnMap As Object
    
    ' 設定シートからBacklogのURLとAPIキーを取得
    Set configSht = ThisWorkbook.Worksheets("config")
    backlogURL = configSht.Range("B1").value
    apiKey = configSht.Range("B2").value
    projectId = configSht.Range("B3").value
    milestoneId = configSht.Range("B4").value
    apiEndpoint = "api/v2/issues?"
    
    ' APIリクエストURLの構築
    ' 例：projectId[]=531908&milestoneId[]=1156331"
    url = backlogURL & apiEndpoint & API_KEY_NAME & "=" & apiKey & "&count=" & MAX_ISSUES
    ' projectIdが空でない場合、URLに追加
    If Len(projectId) > 0 Then
        url = url & "&projectId[]=" & WorksheetFunction.EncodeURL(projectId)
    End If
    
    ' milestoneIdが空でない場合、URLに追加
    If Len(milestoneId) > 0 Then
        url = url & "&milestoneId[]=" & WorksheetFunction.EncodeURL(milestoneId)
    End If
    
    ' HTTPリクエストの準備と送信
    Set http = CreateObject("MSXML2.XMLHTTP")
    http.Open "GET", url, False
    http.send
    
    ' APIレスポンスの処理
    If http.Status = 200 Then
        response = http.responseText
        Debug.Print "==========================http.responseTextレスポンスの表示=========================="
        Debug.Print http.responseText
        
        ' 課題一覧を表示するシートの準備
        Set issueSht = ThisWorkbook.Worksheets("issues")
        issueSht.Cells.Clear
        
        ' ヘッダー行の設定と列マップの作成
        Set columnMap = SetHeaders(issueSht)
        
        ' レスポンスを個別の課題データに分割
        issues = Split(response, "]},{")
        ReDim issueData(1 To UBound(issues) + 1, 1 To columnMap.Count)
        
        ' 各課題データの処理
        For i = 0 To UBound(issues)
            ProcessIssue issues(i), issueData, i + 1, columnMap
            Debug.Print "=====メッセージにて課題を表示====="
            Debug.Print issues(i)
        Next i
        
        ' データをシートに書き込み
        WriteDataToSheet issueSht, issueData
        
        ' 列幅の自動調整
        ' issueSht.UsedRange.Columns.AutoFit
        
        MsgBox "課題一覧を取得しました。", vbInformation
    Else
        Err.Raise vbObjectError + 1, , "APIエラー: ステータスコード " & http.Status
    End If
    
    Exit Sub

ErrorHandler:
    MsgBox "エラーが発生しました: " & Err.Description, vbCritical
End Sub


Private Function SetHeaders(sht As Worksheet) As Object
    Dim columnMap As Object
    Dim headers() As Variant
    Dim i As Long, col As Long
    
    'エクセルに表示する属性
    Set columnMap = CreateObject("Scripting.Dictionary")
    headers = Array(COL_ID, COL_ISSUE_KEY, COL_issueType, COL_SUMMARY, COL_description, COL_STATUS, COL_ASSIGNEE, COL_START_DATE, COL_DUE_DATE, COL_customFields)
    'メッセージにて内容の表示
    
    col = 1
    For i = LBound(headers) To UBound(headers)
        If Len(headers(i)) > 0 Then
            sht.Cells(1, col).value = headers(i)
            columnMap.Add headers(i), col
            col = col + 1
        End If
    Next i
    
    Set SetHeaders = columnMap
End Function

Private Sub ProcessIssue(issue As String, ByRef data() As Variant, row As Long, columnMap As Object)
    If columnMap.Exists(COL_ID) Then data(row, columnMap(COL_ID)) = ExtractValue(issue, "id")
    If columnMap.Exists(COL_projectId) Then data(row, columnMap(COL_projectId)) = ExtractValue(issue, "projectId")
    If columnMap.Exists(COL_ISSUE_KEY) Then data(row, columnMap(COL_ISSUE_KEY)) = ExtractValue(issue, "issueKey")
    If columnMap.Exists(COL_issueType) Then data(row, columnMap(COL_issueType)) = ExtractNestedValue(issue, "issueType", "name")
    If columnMap.Exists(COL_SUMMARY) Then data(row, columnMap(COL_SUMMARY)) = ExtractValue(issue, "summary")
    If columnMap.Exists(COL_description) Then data(row, columnMap(COL_description)) = ExtractValue(issue, "description")
    If columnMap.Exists(COL_STATUS) Then data(row, columnMap(COL_STATUS)) = ExtractNestedValue(issue, "status", "name")
    If columnMap.Exists(COL_ASSIGNEE) Then data(row, columnMap(COL_ASSIGNEE)) = ExtractNestedValue(issue, "assignee", "name")
    If columnMap.Exists(COL_START_DATE) Then data(row, columnMap(COL_START_DATE)) = ConvertDateFormat(ExtractValue(issue, "startDate"))
    If columnMap.Exists(COL_DUE_DATE) Then data(row, columnMap(COL_DUE_DATE)) = ConvertDateFormat(ExtractValue(issue, "dueDate"))
    If columnMap.Exists(COL_customFields) Then data(row, columnMap(COL_customFields)) = ExtractValue(issue, "customFields")
End Sub



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


Private Function ExtractNestedValue(jsonString As String, parentKey As String, childKey As String) As String
    Dim parentValue As String
    parentValue = ExtractValue(jsonString, parentKey)
    If Left(parentValue, 1) = "{" Then
        ExtractNestedValue = ExtractValue(parentValue, childKey)
    Else
        ExtractNestedValue = parentValue
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

