import cv2
import numpy as np

img_path=r"I:\EDA\MyLib\PCIE logo\sbk.webp"
img=cv2.imread(img_path,cv2.IMREAD_UNCHANGED)

if img is None:
    print("读取图片错误！请重新选择！\n")
else:
    h,w,c=img.shape
    if c==4:
        print(f"该图片通道数:{c}")
        print("输入Logo分割的bgr值：\n")
        b_in = int(input())
        g_in = int(input())
        r_in = int(input())
        print(b_in)
        print(g_in)
        print(r_in)
        new_img = np.zeros((h,w,3),dtype=np.uint8)
        for y in range(h):
            for x in range(w):
                b=img[y,x,0]
                g=img[y,x,1]
                r=img[y,x,2]
                a=img[y,x,3]
            # print(b)
            # print(g)
            # print(b)
                if a==0 or  b>b_in and g>g_in and r>r_in:
                    new_img[y, x, 0] = 255
                    new_img[y, x, 1] = 255
                    new_img[y, x, 2] = 255
                else:
                    new_img[y,x,0]=32
                    new_img[y,x,1]=32
                    new_img[y,x,2]=32

    if c==3:
        print(f"该图片通道数:{c}")
        print("输入Logo分割的bgr值：\n")
        b_in = int(input())
        g_in = int(input())
        r_in = int(input())
        print(b_in)
        print(g_in)
        print(r_in)

        new_img = np.zeros((h, w, 3), dtype=np.uint8)
        for y in range(h):
            for x in range(w):
                b = img[y, x, 0]
                g = img[y, x, 1]
                r = img[y, x, 2]

                if ( b>b_in and g>g_in and r>r_in):
                    new_img[y, x, 0] = 255
                    new_img[y, x, 1] = 255
                    new_img[y, x, 2] = 255

                else:
                    new_img[y, x, 0] = 32
                    new_img[y, x, 1] = 32
                    new_img[y, x, 2] = 32


    # print(h)
    # print(w)
    # print(c)


    bmp_save_path = r"I:\EDA\MyLib\PCIE logo\PCIE_logo_bmp.bmp"
    cv2.imwrite(bmp_save_path, new_img)
    print("✅ BMP 已保存:", bmp_save_path)
    cv2.imshow("PCIE logo", new_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()






















