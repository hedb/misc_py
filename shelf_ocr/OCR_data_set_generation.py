
# install package pillow
from PIL import Image, ImageDraw, ImageFont, ImageOps
import random



rect_size = RS = 100
letter_size = LS = 40

def main():

    bad_fonts_set = set(bad_fonts)
    good_fonts = [value for value in fonts if value not in bad_fonts_set]

    for i in range(0,10000):

        try :
            background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            img = Image.new('RGB', (RS, RS), color=background_color)
            font = good_fonts[i%len(good_fonts)]
            fnt = ImageFont.truetype(font, LS)

            pos = (random.randint(0,RS - 2*LS) ,random.randint(0,RS - 2*LS))
            col = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

            col_distance = (background_color[0]-col[0])**2 + (background_color[1]-col[1])**2 + (background_color[2]-col[2])**2
            if (col_distance < 1000):
                print('quitting because of close colors {},{},{}'.format(background_color,col,col_distance))
                continue

            char = chr(i%26+97)

            tmp_txt_image = Image.new('L', (LS*2, LS*2))
            d1 = ImageDraw.Draw(tmp_txt_image)
            d1.text((0,0), char, font=fnt, fill=255)
            tmp_txt_image_rotated = tmp_txt_image.rotate(random.randint(0,90)-45, expand=1)
            img.paste(ImageOps.colorize(tmp_txt_image_rotated, (0, 0, 0), col), pos, tmp_txt_image_rotated)

            # d = ImageDraw.Draw(img)
            # d.text(pos, char, font=fnt, fill=col)

            print( 'printing {}, using {} at {}. background:{},col:{},distance:{}'.format(i,font,pos,background_color,col,col_distance))
            img.save('C:/Users/hedbn/Desktop/shelf_ocr/training_sets/one_letter/{}.png'.format(str(char) + "_"+ str(i)))
        except Exception as exception:
            print ( "Error " + type(exception).__name__ + " with " + font)
            # raise exception




bad_fonts = [
    'C:/Windows/WinSxS/amd64_microsoft-windows-bioenrollment.appxmain_31bf3856ad364e35_10.0.16299.98_none_23321f22674599bb/BioMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-fileexplorer.appxmain_31bf3856ad364e35_10.0.16299.15_none_8c575bad6e8f346f/BitMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-f..-truetype-wingdings_31bf3856ad364e35_10.0.16299.15_none_4c17c1a1fdd2616d/wingding.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-ecapp.appxmain_31bf3856ad364e35_10.0.16299.15_none_1ffc7551fd4a2c5f/ECMDL2.ttf','C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-segoeui_31bf3856ad364e35_10.0.16299.15_none_f3a82fab83612192/segmdl2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-inputapp.appxmain_31bf3856ad364e35_10.0.16299.251_none_90b8eeb33a6e875f/HandwritingMixedInput.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-inputapp.appxmain_31bf3856ad364e35_10.0.16299.251_none_90b8eeb33a6e875f/CloudAnimation.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-inputapp.appxmain_31bf3856ad364e35_10.0.16299.251_none_90b8eeb33a6e875f/GetSMDL.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-microsoftedge_31bf3856ad364e35_10.0.16299.371_none_1ea00bbb5b039194/ReadMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-microsoftedge_31bf3856ad364e35_10.0.16299.371_none_1ea00bbb5b039194/BrowserMDL.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-ui-shellcommon_31bf3856ad364e35_10.0.16299.371_none_ddf60e6c5e1998d7/BitMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-xbox-gamecallableui.toolkit_31bf3856ad364e35_10.0.16299.15_none_cc1cad43e3dd2f9e/segxsym.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-ui-shellcommon_31bf3856ad364e35_10.0.16299.371_none_ddf60e6c5e1998d7/CoreMDL2.1.69.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-marlett_31bf3856ad364e35_10.0.16299.15_none_7141235f7075376c/marlett.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-c..riencehost.appxmain_31bf3856ad364e35_10.0.16299.248_none_104835fdb8656dc7/OOBMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-c..ssets.fonts.cortana_31bf3856ad364e35_10.0.16299.15_none_634416f9c14d024b/BroMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-h..icfirstrun.appxmain_31bf3856ad364e35_10.0.16299.125_none_806ae10a1205b699/HoloMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-holomd2_31bf3856ad364e35_10.0.16299.15_none_be41e811bd7aa8c8/holomdl2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-kor-boot_31bf3856ad364e35_10.0.16299.15_none_7db3ac3e0644ff44/kor_boot.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-symbol_31bf3856ad364e35_10.0.16299.15_none_f210924ac17542c1/symbol.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-i..ntrolpanel.appxmain_31bf3856ad364e35_10.0.16299.371_none_282657b001ebd9e9/SetMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-i..ntrolpanel.appxmain_31bf3856ad364e35_10.0.16299.371_none_282657b001ebd9e9/MemMDL2.2.2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-ui-biofeedback-library_31bf3856ad364e35_10.0.16299.15_none_24f4dc1db0cf43ac/NUIMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-oobe-machine-dui_31bf3856ad364e35_10.0.16299.248_none_ee6ae3a46e260348/StrgMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-xbox-gamecallableui.appxmain_31bf3856ad364e35_10.0.16299.15_none_460c0abd587741da/segxsym.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-cht-boot_31bf3856ad364e35_10.0.16299.15_none_e1024eb99a40f32b/cht_boot.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-c..ssets.fonts.cortana_31bf3856ad364e35_10.0.16299.15_none_634416f9c14d024b/SegoeUISoundlines.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-ui-pcshell_31bf3856ad364e35_10.0.16299.251_none_221c9f8721a31ca8/SharMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-eng-boot_31bf3856ad364e35_10.0.16299.15_none_677f47b71f57202c/wgl4_boot.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-ui-shellcommon_31bf3856ad364e35_10.0.16299.371_none_ddf60e6c5e1998d7/SharMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-c..ssets.fonts.cortana_31bf3856ad364e35_10.0.16299.15_none_634416f9c14d024b/StrgMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-s..hreshold-adminflows_31bf3856ad364e35_10.0.16299.248_none_2e3bdbcd88a86be4/SetMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-jpn-boot_31bf3856ad364e35_10.0.16299.15_none_ac08565e9ad620e2/jpn_boot.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-o..tiveportal.appxmain_31bf3856ad364e35_10.0.16299.15_none_652b3fdd2bb5ce31/BrowserMDL.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-mapcontrol_31bf3856ad364e35_10.0.16299.334_none_20eba9cb7553f181/Bing_Maps_Symbol.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-chs-boot_31bf3856ad364e35_10.0.16299.15_none_f7cfe9f18099a48c/chs_boot.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-webdings_31bf3856ad364e35_10.0.16299.15_none_d1f2f2ca31f64260/webdings.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-lockapp.appxmain_31bf3856ad364e35_10.0.16299.15_none_0a5c3e7b45164e8c/LockMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-i..ntrolpanel.appxmain_31bf3856ad364e35_10.0.16299.371_none_282657b001ebd9e9/BitMDL2.ttf',
    'C:/Windows/WinSxS/amd64_microsoft-windows-c..ssets.fonts.cortana_31bf3856ad364e35_10.0.16299.15_none_634416f9c14d024b/CortMDL2.ttf'


]


fonts = [
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-rod_31bf3856ad364e35_10.0.16299.15_none_b1059a5b25308e3c/rod.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-miriam_31bf3856ad364e35_10.0.16299.15_none_4271d85d37129d24/mriam.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-miriam_31bf3856ad364e35_10.0.16299.15_none_4271d85d37129d24/mriamc.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-frankruehl_31bf3856ad364e35_10.0.16299.15_none_211a67b8525182e1/frank.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-narkisim_31bf3856ad364e35_10.0.16299.15_none_c8f5991b78b9cba9/nrkis.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..-truetype-levenimmt_31bf3856ad364e35_10.0.16299.15_none_a77b75cfb0d2b41e/lvnm.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..-truetype-levenimmt_31bf3856ad364e35_10.0.16299.15_none_a77b75cfb0d2b41e/lvnmbd.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-gisha_31bf3856ad364e35_10.0.16299.15_none_63af1815d0b7b9f3/gisha.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-gisha_31bf3856ad364e35_10.0.16299.15_none_63af1815d0b7b9f3/gishabd.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-aharonibold_31bf3856ad364e35_10.0.16299.15_none_a683332bd1299d04/ahronbd.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-david_31bf3856ad364e35_10.0.16299.15_none_7c024afaf7e5f5fb/david.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-david_31bf3856ad364e35_10.0.16299.15_none_7c024afaf7e5f5fb/davidbd.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-mapcontrol_31bf3856ad364e35_10.0.16299.334_none_20eba9cb7553f181/Bing_Maps_Symbol.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-chs-boot_31bf3856ad364e35_10.0.16299.15_none_f7cfe9f18099a48c/chs_boot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-chs-boot_31bf3856ad364e35_10.0.16299.15_none_f7cfe9f18099a48c/msyhn_boot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-chs-boot_31bf3856ad364e35_10.0.16299.15_none_f7cfe9f18099a48c/msyh_boot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-eng-boot_31bf3856ad364e35_10.0.16299.15_none_677f47b71f57202c/segmono_boot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-eng-boot_31bf3856ad364e35_10.0.16299.15_none_677f47b71f57202c/segoen_slboot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-eng-boot_31bf3856ad364e35_10.0.16299.15_none_677f47b71f57202c/segoe_slboot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-eng-boot_31bf3856ad364e35_10.0.16299.15_none_677f47b71f57202c/wgl4_boot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-jpn-boot_31bf3856ad364e35_10.0.16299.15_none_ac08565e9ad620e2/jpn_boot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-jpn-boot_31bf3856ad364e35_10.0.16299.15_none_ac08565e9ad620e2/meiryon_boot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-jpn-boot_31bf3856ad364e35_10.0.16299.15_none_ac08565e9ad620e2/meiryo_boot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-kor-boot_31bf3856ad364e35_10.0.16299.15_none_7db3ac3e0644ff44/kor_boot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-kor-boot_31bf3856ad364e35_10.0.16299.15_none_7db3ac3e0644ff44/malgunn_boot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-kor-boot_31bf3856ad364e35_10.0.16299.15_none_7db3ac3e0644ff44/malgun_boot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-bioenrollment.appxmain_31bf3856ad364e35_10.0.16299.15_none_23527fb6672d5cb0/BioMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-bioenrollment.appxmain_31bf3856ad364e35_10.0.16299.98_none_23321f22674599bb/BioMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-c..riencehost.appxmain_31bf3856ad364e35_10.0.16299.15_none_25a4a4c4bec46919/OOBMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-c..riencehost.appxmain_31bf3856ad364e35_10.0.16299.98_none_25844430bedca624/OOBMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-ecapp.appxmain_31bf3856ad364e35_10.0.16299.15_none_1ffc7551fd4a2c5f/ECMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..-microsoftsansserif_31bf3856ad364e35_10.0.16299.15_none_4c0630c7b92f1a39/micross.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..-truetype-newtailue_31bf3856ad364e35_10.0.16299.15_none_d44fb1899b86e1c9/ntailu.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..-truetype-nirmalaui_31bf3856ad364e35_10.0.16299.15_none_2887929de11a5dd1/NirmalaB.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..-truetype-nirmalaui_31bf3856ad364e35_10.0.16299.15_none_2887929de11a5dd1/NirmalaS.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..-truetype-tailebold_31bf3856ad364e35_10.0.16299.15_none_ce8548539ad1d623/taileb.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..-truetype-wingdings_31bf3856ad364e35_10.0.16299.15_none_4c17c1a1fdd2616d/wingding.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..e-microsofthimalaya_31bf3856ad364e35_10.0.16299.15_none_2b1eebdcaccc90eb/himalaya.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..e-nirmalaui_regular_31bf3856ad364e35_10.0.16299.15_none_90aeead151ae0286/Nirmala.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..eelawadeeui_regular_31bf3856ad364e35_10.0.16299.15_none_827f6bd605d3ea09/LeelawUI.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..etype-lucidaconsole_31bf3856ad364e35_10.0.16299.15_none_22331e2be9df41c6/lucon.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..etype-newtailuebold_31bf3856ad364e35_10.0.16299.15_none_ca0c4495e348d5a4/ntailub.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..etype-timesnewroman_31bf3856ad364e35_10.0.16299.15_none_005bb2ea0a7bb6a0/times.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..etype-timesnewroman_31bf3856ad364e35_10.0.16299.15_none_005bb2ea0a7bb6a0/timesbd.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..etype-timesnewroman_31bf3856ad364e35_10.0.16299.15_none_005bb2ea0a7bb6a0/timesbi.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..etype-timesnewroman_31bf3856ad364e35_10.0.16299.15_none_005bb2ea0a7bb6a0/timesi.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..i_italicssupplement_31bf3856ad364e35_10.0.16299.15_none_c30e2d3119917165/seguibli.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..i_italicssupplement_31bf3856ad364e35_10.0.16299.15_none_c30e2d3119917165/seguili.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..i_italicssupplement_31bf3856ad364e35_10.0.16299.15_none_c30e2d3119917165/seguisbi.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..i_italicssupplement_31bf3856ad364e35_10.0.16299.15_none_c30e2d3119917165/seguisli.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..lgungothicsemilight_31bf3856ad364e35_10.0.16299.15_none_c25391504dd5a7d1/malgunsl.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..pe-malgungothicbold_31bf3856ad364e35_10.0.16299.15_none_086f765286a7e7f0/malgunbd.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..pe-palatinolinotype_31bf3856ad364e35_10.0.16299.15_none_729009376ca019f3/pala.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..pe-palatinolinotype_31bf3856ad364e35_10.0.16299.15_none_729009376ca019f3/palab.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..pe-palatinolinotype_31bf3856ad364e35_10.0.16299.15_none_729009376ca019f3/palabi.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..pe-palatinolinotype_31bf3856ad364e35_10.0.16299.15_none_729009376ca019f3/palai.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-bahnschrift_31bf3856ad364e35_10.0.16299.15_none_5c9ae5b9da5e3e1f/bahnschrift.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-comicsansms_31bf3856ad364e35_10.0.16299.15_none_ff414fb5ab8706ef/comic.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-comicsansms_31bf3856ad364e35_10.0.16299.15_none_ff414fb5ab8706ef/comicbd.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-comicsansms_31bf3856ad364e35_10.0.16299.15_none_ff414fb5ab8706ef/comici.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-comicsansms_31bf3856ad364e35_10.0.16299.15_none_ff414fb5ab8706ef/comicz.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-myanmartext_31bf3856ad364e35_10.0.16299.15_none_7bd46d41bc7b1f61/mmrtext.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-phagspabold_31bf3856ad364e35_10.0.16299.15_none_a7e51e95142f6dd2/phagspab.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-segoescript_31bf3856ad364e35_10.0.16299.15_none_f7b104905e331351/segoesc.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-segoescript_31bf3856ad364e35_10.0.16299.15_none_f7b104905e331351/segoescb.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-trebuchetms_31bf3856ad364e35_10.0.16299.15_none_a0acb2d3f8cc9b77/trebuc.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-trebuchetms_31bf3856ad364e35_10.0.16299.15_none_a0acb2d3f8cc9b77/trebucbd.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-trebuchetms_31bf3856ad364e35_10.0.16299.15_none_a0acb2d3f8cc9b77/trebucbi.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-trebuchetms_31bf3856ad364e35_10.0.16299.15_none_a0acb2d3f8cc9b77/trebucit.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-arialblack_31bf3856ad364e35_10.0.16299.15_none_0c37f755d8180e15/ariblk.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-constantia_31bf3856ad364e35_10.0.16299.15_none_2df368117addb1e5/constan.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-constantia_31bf3856ad364e35_10.0.16299.15_none_2df368117addb1e5/constanb.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-constantia_31bf3856ad364e35_10.0.16299.15_none_2df368117addb1e5/constani.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-constantia_31bf3856ad364e35_10.0.16299.15_none_2df368117addb1e5/constanz.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-couriernew_31bf3856ad364e35_10.0.16299.15_none_f92f79031e5f6a1e/cour.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-couriernew_31bf3856ad364e35_10.0.16299.15_none_f92f79031e5f6a1e/courbd.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-couriernew_31bf3856ad364e35_10.0.16299.15_none_f92f79031e5f6a1e/courbi.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-couriernew_31bf3856ad364e35_10.0.16299.15_none_f92f79031e5f6a1e/couri.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-ebrimabold_31bf3856ad364e35_10.0.16299.15_none_543a6e9aaf8e3b44/ebrimabd.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-gadugibold_31bf3856ad364e35_10.0.16299.15_none_a30c26e9235e1eb9/gadugib.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-lucidasans_31bf3856ad364e35_10.0.16299.15_none_97dfb19af888c6d6/l_10646.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-segoeprint_31bf3856ad364e35_10.0.16299.15_none_1780a38d6dadc1d1/segoepr.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..type-franklingothic_31bf3856ad364e35_10.0.16299.15_none_ad470155297f0308/framd.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..type-franklingothic_31bf3856ad364e35_10.0.16299.15_none_ad470155297f0308/framdit.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..type-mongolianbaiti_31bf3856ad364e35_10.0.16299.15_none_2689f2a977ae91e2/monbaiti.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..type-segoeprintbold_31bf3856ad364e35_10.0.16299.15_none_8f25289478b6572e/segoeprb.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..uetype-javanesetext_31bf3856ad364e35_10.0.16299.15_none_20526bdcbb961e01/javatext.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..uetype-leelawadeeui_31bf3856ad364e35_10.0.16299.15_none_112915c5fd1678c6/LeelaUIb.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..uetype-leelawadeeui_31bf3856ad364e35_10.0.16299.15_none_112915c5fd1678c6/LeelUIsl.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..uetype-malgungothic_31bf3856ad364e35_10.0.16299.15_none_283c0a6a374e2e1f/malgun.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ype-myanmartextbold_31bf3856ad364e35_10.0.16299.15_none_af576fdb3a33303c/mmrtextb.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..ype-segoeui_regular_31bf3856ad364e35_10.0.16299.15_none_977724ac08805777/segoeui.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-fileexplorer.appxmain_31bf3856ad364e35_10.0.16299.15_none_8c575bad6e8f346f/BitMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-arial_31bf3856ad364e35_10.0.16299.15_none_956f9c221e7f8716/arial.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-arial_31bf3856ad364e35_10.0.16299.15_none_956f9c221e7f8716/arialbd.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-arial_31bf3856ad364e35_10.0.16299.15_none_956f9c221e7f8716/arialbi.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-arial_31bf3856ad364e35_10.0.16299.15_none_956f9c221e7f8716/ariali.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-calibri_31bf3856ad364e35_10.0.16299.15_none_0d92593f60e8ffa5/calibri.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-calibri_31bf3856ad364e35_10.0.16299.15_none_0d92593f60e8ffa5/calibrib.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-calibri_31bf3856ad364e35_10.0.16299.15_none_0d92593f60e8ffa5/calibrii.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-calibri_31bf3856ad364e35_10.0.16299.15_none_0d92593f60e8ffa5/calibril.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-calibri_31bf3856ad364e35_10.0.16299.15_none_0d92593f60e8ffa5/calibrili.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-calibri_31bf3856ad364e35_10.0.16299.15_none_0d92593f60e8ffa5/calibriz.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-cambria_31bf3856ad364e35_10.0.16299.15_none_158dcac875350ae6/cambriab.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-cambria_31bf3856ad364e35_10.0.16299.15_none_158dcac875350ae6/cambriai.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-cambria_31bf3856ad364e35_10.0.16299.15_none_158dcac875350ae6/cambriaz.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-candara_31bf3856ad364e35_10.0.16299.15_none_0e2b661393752913/Candara.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-candara_31bf3856ad364e35_10.0.16299.15_none_0e2b661393752913/Candarab.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-candara_31bf3856ad364e35_10.0.16299.15_none_0e2b661393752913/Candarai.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-candara_31bf3856ad364e35_10.0.16299.15_none_0e2b661393752913/Candaraz.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-consolas_31bf3856ad364e35_10.0.16299.15_none_8cdb7f071676787d/consola.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-consolas_31bf3856ad364e35_10.0.16299.15_none_8cdb7f071676787d/consolab.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-consolas_31bf3856ad364e35_10.0.16299.15_none_8cdb7f071676787d/consolai.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-consolas_31bf3856ad364e35_10.0.16299.15_none_8cdb7f071676787d/consolaz.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-corbel_31bf3856ad364e35_10.0.16299.15_none_f595b9d86fd9fd88/corbel.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-corbel_31bf3856ad364e35_10.0.16299.15_none_f595b9d86fd9fd88/corbelb.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-corbel_31bf3856ad364e35_10.0.16299.15_none_f595b9d86fd9fd88/corbeli.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-corbel_31bf3856ad364e35_10.0.16299.15_none_f595b9d86fd9fd88/corbelz.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-ebrima_31bf3856ad364e35_10.0.16299.15_none_f167faa0cd2d783b/ebrima.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-gabriola_31bf3856ad364e35_10.0.16299.15_none_ab20acf1f84d0798/Gabriola.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-georgia_31bf3856ad364e35_10.0.16299.15_none_53e217acec99e21b/georgia.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-georgia_31bf3856ad364e35_10.0.16299.15_none_53e217acec99e21b/georgiab.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-georgia_31bf3856ad364e35_10.0.16299.15_none_53e217acec99e21b/georgiai.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-georgia_31bf3856ad364e35_10.0.16299.15_none_53e217acec99e21b/georgiaz.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-impact_31bf3856ad364e35_10.0.16299.15_none_6c3a309de435766b/impact.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-marlett_31bf3856ad364e35_10.0.16299.15_none_7141235f7075376c/marlett.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-mvboli_31bf3856ad364e35_10.0.16299.15_none_95da2a1cb90cc786/mvboli.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-phagspa_31bf3856ad364e35_10.0.16299.15_none_95bb9d3e6aa81c4b/phagspa.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-segoeui_31bf3856ad364e35_10.0.16299.15_none_f3a82fab83612192/segmdl2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-segoeui_31bf3856ad364e35_10.0.16299.15_none_f3a82fab83612192/segoeuib.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-segoeui_31bf3856ad364e35_10.0.16299.15_none_f3a82fab83612192/segoeuii.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-segoeui_31bf3856ad364e35_10.0.16299.15_none_f3a82fab83612192/segoeuil.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-segoeui_31bf3856ad364e35_10.0.16299.15_none_f3a82fab83612192/segoeuisl.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-segoeui_31bf3856ad364e35_10.0.16299.15_none_f3a82fab83612192/segoeuiz.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-segoeui_31bf3856ad364e35_10.0.16299.15_none_f3a82fab83612192/seguibl.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-segoeui_31bf3856ad364e35_10.0.16299.15_none_f3a82fab83612192/seguiemj.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-segoeui_31bf3856ad364e35_10.0.16299.15_none_f3a82fab83612192/seguihis.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-segoeui_31bf3856ad364e35_10.0.16299.15_none_f3a82fab83612192/seguisb.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-segoeui_31bf3856ad364e35_10.0.16299.15_none_f3a82fab83612192/seguisym.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-simsunb_31bf3856ad364e35_10.0.16299.15_none_b3e6b5e88d144740/simsunb.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-sylfaen_31bf3856ad364e35_10.0.16299.15_none_819ade4958529ca9/sylfaen.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-symbol_31bf3856ad364e35_10.0.16299.15_none_f210924ac17542c1/symbol.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-tahoma_31bf3856ad364e35_10.0.16299.15_none_52b8969ee5c7eaa3/tahoma.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-tahoma_31bf3856ad364e35_10.0.16299.15_none_52b8969ee5c7eaa3/tahomabd.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-taile_31bf3856ad364e35_10.0.16299.15_none_ae4aca9e20bad18a/taile.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-verdana_31bf3856ad364e35_10.0.16299.15_none_e1654f127052576a/verdana.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-verdana_31bf3856ad364e35_10.0.16299.15_none_e1654f127052576a/verdanab.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-verdana_31bf3856ad364e35_10.0.16299.15_none_e1654f127052576a/verdanai.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-verdana_31bf3856ad364e35_10.0.16299.15_none_e1654f127052576a/verdanaz.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-webdings_31bf3856ad364e35_10.0.16299.15_none_d1f2f2ca31f64260/webdings.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-yibaiti_31bf3856ad364e35_10.0.16299.15_none_7b2dec3c2bc2b374/msyi.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-h..icfirstrun.appxmain_31bf3856ad364e35_10.0.16299.125_none_806ae10a1205b699/HoloMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-h..icfirstrun.appxmain_31bf3856ad364e35_10.0.16299.15_none_95b4b2bd187232f9/HoloMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-i..ntrolpanel.appxmain_31bf3856ad364e35_10.0.16299.15_none_3daa365b082c35a2/BitMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-i..ntrolpanel.appxmain_31bf3856ad364e35_10.0.16299.15_none_3daa365b082c35a2/MemMDL2.2.2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-i..ntrolpanel.appxmain_31bf3856ad364e35_10.0.16299.15_none_3daa365b082c35a2/SetMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-inputapp.appxmain_31bf3856ad364e35_10.0.16299.125_none_90dd5db93a529bc1/CloudAnimation.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-inputapp.appxmain_31bf3856ad364e35_10.0.16299.125_none_90dd5db93a529bc1/GetSMDL.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-inputapp.appxmain_31bf3856ad364e35_10.0.16299.125_none_90dd5db93a529bc1/HandwritingMixedInput.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-inputapp.appxmain_31bf3856ad364e35_10.0.16299.125_none_90dd5db93a529bc1/SegoeHWP.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-inputapp.appxmain_31bf3856ad364e35_10.0.16299.15_none_a6272f6c40bf1821/CloudAnimation.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-inputapp.appxmain_31bf3856ad364e35_10.0.16299.15_none_a6272f6c40bf1821/GetSMDL.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-inputapp.appxmain_31bf3856ad364e35_10.0.16299.15_none_a6272f6c40bf1821/HandwritingMixedInput.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-inputapp.appxmain_31bf3856ad364e35_10.0.16299.15_none_a6272f6c40bf1821/SegoeHWP.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-lockapp.appxmain_31bf3856ad364e35_10.0.16299.15_none_0a5c3e7b45164e8c/LockMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-mapcontrol_31bf3856ad364e35_10.0.16299.15_none_364147e87bb770f9/Bing_Maps_Symbol.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-microsoftedge_31bf3856ad364e35_10.0.16299.125_none_1eda18b35ad770ed/BrowserMDL.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-microsoftedge_31bf3856ad364e35_10.0.16299.125_none_1eda18b35ad770ed/ReadMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-microsoftedge_31bf3856ad364e35_10.0.16299.15_none_3423ea666143ed4d/BrowserMDL.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-microsoftedge_31bf3856ad364e35_10.0.16299.15_none_3423ea666143ed4d/ReadMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-o..tiveportal.appxmain_31bf3856ad364e35_10.0.16299.15_none_652b3fdd2bb5ce31/BrowserMDL.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-oobe-machine-dui_31bf3856ad364e35_10.0.16299.15_none_03c7526b7484fe9a/StrgMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-oobe-machine-dui_31bf3856ad364e35_10.0.16299.98_none_03a6f1d7749d3ba5/StrgMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-s..hreshold-adminflows_31bf3856ad364e35_10.0.16299.125_none_2e4e78e1889aead6/SetMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-s..hreshold-adminflows_31bf3856ad364e35_10.0.16299.15_none_43984a948f076736/SetMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-ui-biofeedback-library_31bf3856ad364e35_10.0.16299.15_none_24f4dc1db0cf43ac/NUIMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-ui-pcshell_31bf3856ad364e35_10.0.16299.15_none_378ae04027f3ad6a/SharMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-ui-shellcommon_31bf3856ad364e35_10.0.16299.15_none_f379ed176459f490/BitMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-ui-shellcommon_31bf3856ad364e35_10.0.16299.15_none_f379ed176459f490/CoreMDL2.1.69.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-ui-shellcommon_31bf3856ad364e35_10.0.16299.15_none_f379ed176459f490/SharMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-ui-shellcommon_31bf3856ad364e35_10.0.16299.98_none_f3598c836472319b/BitMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-ui-shellcommon_31bf3856ad364e35_10.0.16299.98_none_f3598c836472319b/CoreMDL2.1.69.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-ui-shellcommon_31bf3856ad364e35_10.0.16299.98_none_f3598c836472319b/SharMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-xbox-gamecallableui.appxmain_31bf3856ad364e35_10.0.16299.15_none_460c0abd587741da/segxsym.ttf',
'C:/Windows/WinSxS/amd64_microsoft-xbox-gamecallableui.toolkit_31bf3856ad364e35_10.0.16299.15_none_cc1cad43e3dd2f9e/segxsym.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-microsoftedge_31bf3856ad364e35_10.0.16299.371_none_1ea00bbb5b039194/BrowserMDL.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-microsoftedge_31bf3856ad364e35_10.0.16299.371_none_1ea00bbb5b039194/ReadMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-ui-shellcommon_31bf3856ad364e35_10.0.16299.371_none_ddf60e6c5e1998d7/BitMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-ui-shellcommon_31bf3856ad364e35_10.0.16299.371_none_ddf60e6c5e1998d7/CoreMDL2.1.69.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-ui-shellcommon_31bf3856ad364e35_10.0.16299.371_none_ddf60e6c5e1998d7/SharMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-i..ntrolpanel.appxmain_31bf3856ad364e35_10.0.16299.371_none_282657b001ebd9e9/BitMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-i..ntrolpanel.appxmain_31bf3856ad364e35_10.0.16299.371_none_282657b001ebd9e9/MemMDL2.2.2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-i..ntrolpanel.appxmain_31bf3856ad364e35_10.0.16299.371_none_282657b001ebd9e9/SetMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-cht-boot_31bf3856ad364e35_10.0.16299.15_none_e1024eb99a40f32b/cht_boot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-cht-boot_31bf3856ad364e35_10.0.16299.15_none_e1024eb99a40f32b/msjhn_boot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-b..core-fonts-cht-boot_31bf3856ad364e35_10.0.16299.15_none_e1024eb99a40f32b/msjh_boot.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-c..ssets.fonts.cortana_31bf3856ad364e35_10.0.16299.15_none_634416f9c14d024b/BroMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-c..ssets.fonts.cortana_31bf3856ad364e35_10.0.16299.15_none_634416f9c14d024b/CortMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-c..ssets.fonts.cortana_31bf3856ad364e35_10.0.16299.15_none_634416f9c14d024b/SegoeUISoundlines.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-c..ssets.fonts.cortana_31bf3856ad364e35_10.0.16299.15_none_634416f9c14d024b/StrgMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-gadugi_31bf3856ad364e35_10.0.16299.15_none_072aedde96646786/gadugi.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-font-truetype-holomd2_31bf3856ad364e35_10.0.16299.15_none_be41e811bd7aa8c8/holomdl2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-c..riencehost.appxmain_31bf3856ad364e35_10.0.16299.248_none_104835fdb8656dc7/OOBMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-oobe-machine-dui_31bf3856ad364e35_10.0.16299.248_none_ee6ae3a46e260348/StrgMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-ui-pcshell_31bf3856ad364e35_10.0.16299.251_none_221c9f8721a31ca8/SharMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-s..hreshold-adminflows_31bf3856ad364e35_10.0.16299.248_none_2e3bdbcd88a86be4/SetMDL2.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-couriernew_31bf3856ad364e35_10.0.16299.192_none_e396f6fe182e6550/cour.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-couriernew_31bf3856ad364e35_10.0.16299.192_none_e396f6fe182e6550/courbd.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-couriernew_31bf3856ad364e35_10.0.16299.192_none_e396f6fe182e6550/courbi.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-f..truetype-couriernew_31bf3856ad364e35_10.0.16299.192_none_e396f6fe182e6550/couri.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-inputapp.appxmain_31bf3856ad364e35_10.0.16299.251_none_90b8eeb33a6e875f/CloudAnimation.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-inputapp.appxmain_31bf3856ad364e35_10.0.16299.251_none_90b8eeb33a6e875f/GetSMDL.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-inputapp.appxmain_31bf3856ad364e35_10.0.16299.251_none_90b8eeb33a6e875f/HandwritingMixedInput.ttf',
'C:/Windows/WinSxS/amd64_microsoft-windows-inputapp.appxmain_31bf3856ad364e35_10.0.16299.251_none_90b8eeb33a6e875f/SegoeHWP.ttf'
]

main()