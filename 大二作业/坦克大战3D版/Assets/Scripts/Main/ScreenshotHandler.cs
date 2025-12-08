using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class ScreenshotHandler : MonoBehaviour
{

    public Text feedbackText; // 用于显示提示信息
    public string screenshotFolder = "Screenshots"; // 截图存储路径

    void Start()
    {
        // 确保提示文本开始时是隐藏的
        feedbackText.gameObject.SetActive(false);

        
    }

    public void TakeScreenshot()
    {
        // 启动协程进行截图
        StartCoroutine(CaptureScreenshot());
    }

    private IEnumerator CaptureScreenshot()
    {
        // 确保截图文件夹存在
        if (!System.IO.Directory.Exists(screenshotFolder))
        {
            System.IO.Directory.CreateDirectory(screenshotFolder);
        }

        // 生成截图文件名
        string screenshotName = System.IO.Path.Combine(screenshotFolder, "Screenshot_" + System.DateTime.Now.ToString("yyyyMMdd_HHmmss") + ".png");

        // 捕获屏幕截图
        ScreenCapture.CaptureScreenshot(screenshotName);

        // 等待截图保存完成
        yield return new WaitForEndOfFrame();

        // 显示提示信息
        feedbackText.text = "截图成功，保存至 " + screenshotName;
        feedbackText.gameObject.SetActive(true);

        // 一段时间后隐藏提示信息
        yield return new WaitForSeconds(2f);
        feedbackText.gameObject.SetActive(false);
    }
}