Attribute VB_Name = "Module1"
Option Explicit

'''<summary>
'''モジュールの説明
'''</summary>

'''<summary>
'''かんたんなプロシージャ
'''</summary>
Sub sampleProcedure()
    Debug.Print "sampleProcedure running."
End Sub

'''<summary>
'''かんたんなプライベートプロシージャ
'''</summary>
'''<param name="num">数字</param>
Private Sub samplePrivateProcedure(ByVal num As Integer)
    Debug.Print num
End Sub

'''<summary>
'''名前を呼ぶ文字列を返す関数
'''</summary>
'''<param name="name">名前</param>
'''<returns>名前を呼ぶ文字列</returns>
'''<remarks>注意事項</remarks>
Function sampleFunction(ByVal name As String) As String
    Dim callName As String
    callName = name + "さん"
    Debug.Print "こんにちは、" + callName
    sampleFunction = callName
End Function
