import sys
import os
import shutil
from tkinter import Tk, filedialog
from typing import Literal, Union
import win32gui
import time
import pandas as pd
import xml.etree.ElementTree as ET
import pythoncom
import win32com.client as win32

# CircularImport 오류 출력안함
devnull = open(os.devnull, 'w')
old_stdout = sys.stdout
old_stderr = sys.stderr
sys.stdout = devnull
sys.stderr = devnull

try:
    import win32com.client as win32
finally:
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    devnull.close()


# temp 폴더 삭제
try:
    shutil.rmtree(os.path.join(os.environ["USERPROFILE"], "AppData/Local/Temp/gen_py"))
except FileNotFoundError as e:
    pass

# Type Library 파일 재생성
win32.gencache.EnsureModule('{7D2B6F3C-1D95-4E0C-BF5A-5EE564186FBC}', 0, 1, 0)

class HWP():
    def __init__(self) -> None:
        try:
            self.hwp = win32.gencache.EnsureDispatch("hwpframe.hwpobject")
            self.hwp.XHwpWindows.Item(0).Visible = True
            self.num = 0
            try:
                self.hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
            except:
                pass
        except Exception as e:
            # print(f"HWP 객체 생성 실패: {e}, 재시도합니다.")
            pythoncom.CoUninitialize()
            pythoncom.CoInitialize()
            
            self.hwp = win32.gencache.EnsureDispatch("hwpframe.hwpobject")
            self.hwp.XHwpWindows.Item(0).Visible = True
            self.num = 0
            try:
                self.hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
            except:
                pass
            # self.hwp = None
        time.sleep(0.2)
#----------------------------------------------추가기능----------------------------------------------------------





#----------------------------------------------추가기능----------------------------------------------------------

    # 기본조작

    def add_doc(self:None):
        '새 문서를 연다.'
        return self.hwp.XHwpDocuments.Add(0)  # 0은 새 창, 1은 새 탭
    
    def add_tab(self:None):
        '새 탭을 연다.'
        return self.hwp.XHwpDocuments.Add(1)  # 0은 새 창, 1은 새 탭

    def open(self, path:str):
        '기존 한글파일을 연다.'
        return self.hwp.Open(path)

    def close(self:None):
        '''
        활성화된 한글파일을 저장하지 않고 닫는다.
        단 열려있는 문서가 1개라면, 창이 꺼지지 않는다.
        '''
        self.hwp.Clear(1)
        return self.hwp.XHwpDocuments.Active_XHwpDocument.Close(isDirty=False)

    def save(self:None, save_if_dirty=True):
        """
        현재 편집중인 문서를 저장한다.
        문서의 경로가 지정되어있지 않으면 “새 이름으로 저장” 대화상자가 뜬다.
        """
        return self.hwp.Save(save_if_dirty=save_if_dirty)

    def saveAs(self):
        """
        파일을 이미지와 함께 저장할 수 있도록 하는 메서드.
        파일 저장 대화상자를 사용하여 경로와 이름을 지정합니다.
        """
        # Tkinter 초기화 (GUI 창 숨김)
        root = Tk()
        root.withdraw()

        # 파일 저장 경로와 이름을 지정하는 대화 상자 열기
        file_path = filedialog.asksaveasfilename(
            defaultextension=".hwpx",
            filetypes=[("HWPX files", "*.hwpx"), ("All files", "*.*")],
            title="파일 저장 위치와 이름을 선택하세요."
        )

        # 파일 경로가 선택된 경우에만 실행
        if file_path:
            self.hwp.HAction.GetDefault("PictureSaveAsAll", self.hwp.HParameterSet.HSaveAsImage.HSet)
            self.hwp.HAction.Execute("PictureSaveAsAll", self.hwp.HParameterSet.HSaveAsImage.HSet)
            self.hwp.HAction.GetDefault("FileSaveAs_S", self.hwp.HParameterSet.HFileOpenSave.HSet)
            self.hwp.HParameterSet.HFileOpenSave.HSet.SetItem("FileName", file_path)
            self.hwp.HParameterSet.HFileOpenSave.HSet.SetItem("Format", "HWPX")
            self.hwp.HAction.Execute("FileSaveAs_S", self.hwp.HParameterSet.HFileOpenSave.HSet)

    def save_As(self, path, format="HWPX", arg=""):
        """
        현재 편집중인 문서를 지정한 이름으로 저장한다.
        format, arg의 일반적인 개념에 대해서는 Open()참조.
        "Hwp" 포맷으로 파일 저장 시 arg에 지정할 수 있는 옵션은 다음과 같다.
        "lock:true" - 저장한 후 해당 파일을 계속 오픈한 상태로 lock을 걸지 여부
        "backup:false" - 백업 파일 생성 여부
        "compress:true" - 압축 여부
        "fullsave:false" - 스토리지 파일을 완전히 새로 생성하여 저장
        "prvimage:2" - 미리보기 이미지 (0=off, 1=BMP, 2=GIF)
        "prvtext:1" - 미리보기 텍스트 (0=off, 1=on)
        "autosave:false" - 자동저장 파일로 저장할 지 여부 (TRUE: 자동저장, FALSE: 지정 파일로 저장)
        "export" - 다른 이름으로 저장하지만 열린 문서는 바꾸지 않는다.(lock:false와 함께 설정되어 있을 시 동작)
        여러 개를 한꺼번에 할 경우에는 세미콜론으로 구분하여 연속적으로 사용할 수 있다.
        "lock:TRUE;backup:FALSE;prvtext:1"

        :param path:
            문서 파일의 전체경로

        :param format:
            문서 형식. 생략하면 "HWPX"가 지정된다.

        :param arg:
            세부 옵션. 의미는 format에 지정한 파일 형식에 따라 다르다. 생략하면 빈 문자열이 지정된다.

        :return:
            성공하면 True, 실패하면 False
        """
        if path.lower()[1] != ":":
            path = os.path.join(os.getcwd(), path)
        return self.hwp.SaveAs(Path=path, Format=format, arg=arg)


# 인터페이스 조작하기
    @property
    def XHwpWindows(self:None):
        return self.hwp.XHwpWindows
    
    @property
    def title(self) -> str:  # self의 타입은 생략하거나 HwpController로 지정할 수 있음
        if self.num == 0:
            self.hwp.XHwpDocuments.Item(self.num).SetActive_XHwpDocument()  
            return self.get_active_window_title()
        else:
            self.hwp.XHwpDocuments.Item(self.num).SetActive_XHwpDocument()
            return self.get_active_window_title()

    def maximize_window(self:None):
        """현재 창 최대화"""
        win32gui.ShowWindow(
            self.XHwpWindows.Active_XHwpWindow.WindowHandle, 3)

    def minimize_window(self:None):
        """현재 창 최소화"""
        win32gui.ShowWindow(
            self.XHwpWindows.Active_XHwpWindow.WindowHandle, 6)
    
    def show_window(self:None):
        """백그라운드의 한글파일을 보여줍니다"""
        win32gui.ShowWindow(
            self.XHwpWindows.Active_XHwpWindow.WindowHandle, 5)
    
    def hide_window(self:None):
        """한글파일을 백그라운드로 숨깁니다"""
        win32gui.ShowWindow(
            self.XHwpWindows.Active_XHwpWindow.WindowHandle, 0)

    def quit(self:None):
        """
        한/글을 종료한다.
        단, 저장되지 않은 변경사항이 있는 경우 팝업이 뜨므로
        clear나 save 등의 메서드를 실행한 후에 quit을 실행해야 한다.
        :return:
        """
        self.hwp.XHwpDocuments.Close(isDirty=False)
        self.hwp.Quit()
        del self.hwp    
    
# 페이지 조작하기
    @property
    def page_Count(self): # 제어중인 한글 페이지수를 리턴합니다
        """
        현재 문서의 총 페이지 수를 리턴한다.
        :return:
        """
        return self.hwp.PageCount
    
    @property
    def current_page(self):
        """
        현재 쪽번호를 리턴.
        1페이지에 있다면 1을 리턴한다.
        새쪽번호가 적용되어 있어도
        페이지의 인덱스를 리턴한다.
        :return:
        """
        return self.hwp.XHwpDocuments.Active_XHwpDocument.XHwpDocumentInfo.CurrentPage + 1

    @property
    def page_source(self, format="HWPML2X", option=""):
        '''
        현재 열려있는 한글파일의 xml을 얻어온다.
        soup.select("TEXT > CHAR") 로 모든 텍스트를 추출할 수 있다.
        
        from bs4 import BeautifulSoup

        # XML 데이터를 파싱
        xml = hwp.page_source
        soup = BeautifulSoup(xml, 'xml')

        # 전체 TEXT > CHAR 요소 추출
        all_chars = soup.select("TEXT > CHAR")

        # 표(TABLE) 내부의 TEXT > CHAR 요소 추출
        table_chars = []
        for table in soup.select("TABLE"):
            table_chars.extend(table.select("TEXT > CHAR"))

        # all_chars에서 table_chars에 속하지 않는 요소들만 선택
        outside_table_chars = []

        # all_chars 리스트를 하나씩 순회
        for char in all_chars:
            # 만약 char가 table_chars에 포함되지 않으면
            if char not in table_chars:
                # outside_table_chars 리스트에 추가
                outside_table_chars.append(char)

        # 결과 출력
        for char in outside_table_chars:
            print(char.text)
        '''
        return self.hwp.GetTextFile(Format=format, option=option)

    def page_Copy(self:None):
        """
        쪽 복사
        """
        return self.hwp.HAction.Run("CopyPage")
    
    def page_Paste(self:None):
        """
        쪽 붙여넣기
        """
        return self.hwp.HAction.Run("PastePage")
    
    def page_Delete(self:None):
        """
        쪽 지우기
        """
        return self.hwp.HAction.Run("DeletePage")
    
    def goto_Startpage(self:None):
        '문서의 시작으로 이동한다'
        return self.hwp.HAction.Run("MoveDocBegin")
    
    def goto_Endpage(self:None):
        '문서의 끝으로 이동한다'
        return self.hwp.HAction.Run("MoveDocEnd")

    def goto_page(self, page_index: int | str = 1) -> tuple[int, int]: # 지정한 페이지로 이동합니다.
        """
        새쪽번호와 관계없이 페이지 순서를 통해
        특정 페이지를 찾아가는 메서드.
        1이 1페이지임.
        :param page_index:
        :return: tuple(인쇄기준페이지, 페이지인덱스)
        """
        if int(page_index) > self.hwp.PageCount:
            raise ValueError("입력한 페이지 인덱스가 문서 총 페이지보다 큽니다.")
        elif int(page_index) < 1:
            raise ValueError("1 이상의 값을 입력해야 합니다.")
        self.goto_printpage(page_index)
        cur_page = self.current_page
        if page_index == cur_page:
            pass
        elif page_index < cur_page:
            for _ in range(cur_page - page_index):
                self.MovePageUp()
        else:
            for _ in range(page_index - cur_page):
                self.MovePageDown()
        return self.current_printpage, self.current_page

# 표(셀) 조작하기

    def insert_table(self, rows, cols, treat_as_char: bool = True, width_type=0, height_type=0, header=True, height=0):
        """
        표를 생성하는 메서드.
        기본적으로 rows와 cols만 지정하면 되며,
        용지여백을 제외한 구간에 맞춰 표 너비가 결정된다.
        이는 일반적인 표 생성과 동일한 수치이다.

        아래의 148mm는 종이여백 210mm에서 60mm(좌우 각 30mm)를 뺀 150mm에다가,
        표 바깥여백 각 1mm를 뺀 148mm이다. (TableProperties.Width = 41954)
        각 열의 너비는 5개 기준으로 26mm인데 이는 셀마다 안쪽여백 좌우 각각 1.8mm를 뺀 값으로,
        148 - (1.8 x 10 =) 18mm = 130mm
        그래서 셀 너비의 총 합은 130이 되어야 한다.
        아래의 라인28~32까지 셀너비의 합은 16+36+46+16+16=130
        표를 생성하는 시점에는 표 안팎의 여백을 없애거나 수정할 수 없으므로
        이는 고정된 값으로 간주해야 한다.

        :return:
            표 생성 성공시 True, 실패시 False를 리턴한다.
        """

        pset = self.hwp.HParameterSet.HTableCreation
        self.hwp.HAction.GetDefault("TableCreate", pset.HSet)  # 표 생성 시작
        pset.Rows = rows  # 행 갯수
        pset.Cols = cols  # 열 갯수
        pset.WidthType = width_type  # 너비 지정(0:단에맞춤, 1:문단에맞춤, 2:임의값)
        pset.HeightType = height_type  # 높이 지정(0:자동, 1:임의값)

        sec_def = self.hwp.HParameterSet.HSecDef
        self.hwp.HAction.GetDefault("PageSetup", sec_def.HSet)
        total_width = (
                sec_def.PageDef.PaperWidth - sec_def.PageDef.LeftMargin - sec_def.PageDef.RightMargin - sec_def.PageDef.GutterLen - self.mili_to_hwp_unit(
            2))

        pset.WidthValue = total_width  # 표 너비(근데 영향이 없는 듯)
        if height and height_type == 1:  # 표높이가 정의되어 있으면
            # 페이지 최대 높이 계산
            total_height = (
                    sec_def.PageDef.PaperHeight - sec_def.PageDef.TopMargin - sec_def.PageDef.BottomMargin - sec_def.PageDef.HeaderLen - sec_def.PageDef.FooterLen - self.mili_to_hwp_unit(
                2))
            pset.HeightValue = min(self.hwp.MiliToHwpUnit(height), total_height)  # 표 높이
            pset.CreateItemArray("RowHeight", rows)  # 행 m개 생성
            each_row_height = min((self.mili_to_hwp_unit(height) - self.mili_to_hwp_unit((0.5 + 0.5) * rows)) // rows,
                                  (total_height - self.mili_to_hwp_unit((0.5 + 0.5) * rows)) // rows)
            for i in range(rows):
                pset.RowHeight.SetItem(i, each_row_height)  # 1열
            pset.TableProperties.Height = min(self.MiliToHwpUnit(height),
                                              total_height - self.mili_to_hwp_unit((0.5 + 0.5) * rows))

        pset.CreateItemArray("ColWidth", cols)  # 열 n개 생성
        each_col_width = total_width - self.mili_to_hwp_unit(3.6 * cols)
        for i in range(cols):
            pset.ColWidth.SetItem(i, each_col_width)  # 1열
        # pset.TableProperties.TreatAsChar = treat_as_char  # 글자처럼 취급
        pset.TableProperties.Width = total_width  # self.hwp.MiliToHwpUnit(148)  # 표 너비
        self.hwp.HAction.Execute("TableCreate", pset.HSet)  # 위 코드 실행

        # 글자처럼 취급 여부 적용(treat_as_char)
        ctrl = self.hwp.CurSelectedCtrl or self.hwp.ParentCtrl
        pset = self.hwp.CreateSet("Table")
        pset.SetItem("TreatAsChar", treat_as_char)
        ctrl.Properties = pset

        # 제목 행 여부 적용(header)
        pset = self.hwp.HParameterSet.HShapeObject
        self.hwp.HAction.GetDefault("TablePropertyDialog", pset.HSet)
        pset.ShapeTableCell.Header = header
        # try:
        #     self.hwp.HAction.Execute("TablePropertyDialog", pset.HSet)
        # except:
        #     pass

    def insert_cellfield(self, field : str, option=0, direction="", memo=""):
        """
        현재 마우스커서(캐럿)가 깜빡이는 표의 셀에 셀필드를 생성한다.
        커서상태 or 회색선택상태(F5)에서만 필드삽입이 가능하다.
        필드가 생성되어있다면, 기존 필드에 덮어쓴다.
        :return:
            성공하면 True, 실패하면 False
        """
        if not self.is_cell():
            raise AssertionError("마우스 커서가 표 안에 있지 않습니다.")
        if self.SelectionMode == 0x13:
            pset = self.HParameterSet.HShapeObject
            self.HAction.GetDefault("TablePropertyDialog", pset.HSet)
            pset.HSet.SetItem("ShapeType", 3)
            pset.HSet.SetItem("ShapeCellSize", 0)
            pset.ShapeTableCell.CellCtrlData.name = field
            return self.HAction.Execute("TablePropertyDialog", pset.HSet)
        else:
            return self.hwp.SetCurFieldName(Field=field, option=option, Direction=direction, memo=memo)

    def goto_table(self, table_index:int=1, cell_address:str=''):
        '''
        특정 표 안으로 이동한다.
        index 기본값은 1으로 설정되어있으며,
        다른 표로 이동 시 index값을 늘려주면 된다.              
        '''
        ctrl = self.hwp.HeadCtrl
        table_dict = {}
        index = 1

        # 모든 표를 탐색하며 인덱스와 위치를 저장
        while ctrl:
            if ctrl.UserDesc == '표':
                table_dict[index] = ctrl.GetAnchorPos(0)
                # print(f"Table {index}: Position {ctrl.GetAnchorPos(0)}")
                index += 1
            ctrl = ctrl.Next

        # 선택한 인덱스가 존재하는지 확인하고 이동
        selected_pos = table_dict.get(table_index)
        if selected_pos:
            self.hwp.SetPosBySet(selected_pos)
            self.hwp.FindCtrl()
            self.hwp.HAction.Run('ShapeObjTableSelCell')
            # cell_address가 입력된 경우 해당 셀 주소로 캐럿을 이동
            if cell_address:
                row, col = self.addr_to_tuple(cell_address)  # cell_address를 튜플로 변환

                # 행과 열을 이동
                for move_col in range(col - 1):  # 열 이동
                    self.cell_right()

                for move_row in range(row - 1):  # 행 이동
                    self.cell_down()
            return True
        else:
            print("유효하지 않은 표 인덱스입니다.")

    def delete_table(self, table_index: int = 1):
        '''
        특정 표를 삭제한다.
        기본값은 첫 번째 표(index=1)이며,
        다른 표를 삭제하려면 table_index 값을 조정하면 된다.
        '''
        ctrl = self.hwp.HeadCtrl
        table_dict = {}
        index = 1

        # 모든 표를 탐색하며 인덱스와 위치를 저장
        while ctrl:
            if ctrl.UserDesc == '표':
                table_dict[index] = ctrl.GetAnchorPos(0)
                # print(f"Table {index}: Position {ctrl.GetAnchorPos(0)}")
                index += 1
            ctrl = ctrl.Next

        # 선택한 인덱스가 존재하는지 확인하고 삭제
        selected_pos = table_dict.get(table_index)
        if selected_pos:
            self.hwp.SetPosBySet(selected_pos)
            self.hwp.FindCtrl()
            self.hwp.HAction.Run('Delete')  # 표 삭제 명령 실행
            return True
        else:
            print("유효하지 않은 표 인덱스입니다.")
            return False

    # @property
    def cell_address(self):
        '현재 캐럿위치의 셀 주소를 반환한다.'
        return self.hwp.KeyIndicator()[-1].split(":")[0].replace('(','').replace(')','')

    def cell_out(self):
        '표 내부에 있을 때, 표 밖으로 나간다.'       
        return self.hwp.HAction.Run('Close')
        
    def cell_left(self):
        '표 내부 캐럿을 좌측으로 한칸 이동한다.'
        return self.hwp.HAction.Run("TableLeftCell")

    def cell_right(self):
        '표 내부 캐럿을 우측으로 한칸 이동한다.'
        return self.hwp.HAction.Run("TableRightCell")

    def cell_rightAdd(self):
        '''
        표 내부 캐럿을 우측으로 한칸 이동한다.
        만약 표의 마지막 문단이라면 표를 추가한다.
        '''
        return self.hwp.HAction.Run("TableRightCellAppend")

    def cell_up(self):
        '표 내부 캐럿을 위로 한칸 이동한다.'
        return self.hwp.HAction.Run("TableUpperCell")

    def cell_down(self):
        '표 내부 캐럿을 아래로 한칸 이동한다.'
        return self.hwp.HAction.Run("TableLowerCell")

    def cell_left_end(self):
        '현재 캐럿이 있는 위치를 기준으로 캐럿을 왼쪽 끝으로 이동시킨다.'
        return self.hwp.HAction.Run("TableColBegin")

    def cell_up_end(self):
        '현재 캐럿이 있는 위치를 기준으로 캐럿을 위쪽 끝으로 이동시킨다.'
        return self.hwp.HAction.Run("TableColPageUp")

    def cell_right_end(self):
        '현재 캐럿이 있는 위치를 기준으로 캐럿을 오른쪽 끝으로 이동시킨다.'
        return self.hwp.HAction.Run("TableColEnd")

    def cell_down_end(self):
        '현재 캐럿이 있는 위치를 기준으로 캐럿을 아래쪽 끝으로 이동시킨다.'
        return self.hwp.HAction.Run("TableColPageDown")

# 필드 조작하기
    
    def insert_field(self, field_Name:str, Name:str): # 누름틀 필드 생성
        """
        누름틀 필드를 삽입하는 메서드입니다.

        Parameters:
            field_Name (str): 필드의 이름 
            Name (str): 필드의 내용 또는 방향 
        """
        # InsertFieldTemplate 액션의 기본값을 가져옵니다.
        self.hwp.HAction.GetDefault("InsertFieldTemplate", self.hwp.HParameterSet.HInsertFieldTemplate.HSet)
        
        # 필드 설정
        self.hwp.HParameterSet.HInsertFieldTemplate.TemplateDirection = Name  # 필드의 내용 또는 방향 설정
        self.hwp.HParameterSet.HInsertFieldTemplate.TemplateName = field_Name  # 필드의 이름 설정
        
        # 액션 실행하여 누름틀 필드 삽입
        self.hwp.HAction.Execute("InsertFieldTemplate", self.hwp.HParameterSet.HInsertFieldTemplate.HSet)

    def insert_picture(self, path: str, sizeoption: int=0):
        """
        HWP 문서에 그림을 삽입하는 메서드입니다.

        Parameters:
            path (str): 삽입할 그림 파일의 경로입니다.
            sizeoption (int): 그림의 크기 옵션을 지정합니다.
                - 0: 이미지 원래 크기로 삽입합니다.
                - 2: 셀 안에 있을 때 셀을 채웁니다 (그림 비율 무시).
                - 3: 셀에 맞추되 그림 비율을 유지하여 크기를 변경합니다.

        Returns:
            삽입된 그림 객체를 반환합니다.
        """
        return self.hwp.InsertPicture(path, sizeoption=sizeoption)

    def put_field_text(self, field_Name:str, Text:str):
        '지정한 필드에 넣고싶은 text를 넣습니다'
        return self.hwp.PutFieldText(f"{field_Name}", f"{Text}")  
    
    def get_field_list(self:None):
        '현재 한글파일에 생성된 모든 필드를 리스트로 보여줍니다.'
        return self.hwp.GetFieldList(1).split('')
    
    def get_field_text(self, field_Name:str):
        '선택된 필드의 text를 추출합니다.'
        return self.hwp.GetFieldText(f'{field_Name}')
    
    def goto_field(self, field_Name:str):
        '선택된 필드로 커서(캐럿)를 이동시킵니다.'
        return self.hwp.MoveToField(f'{field_Name}')
    
    def rename_field(self, oldname:str, newname:str):
        """
        지정한 필드의 이름을 바꾼다.
        예를 들어 oldname에 "title{{0}}\x02title{{1}}",
        newname에 "tt1\x02tt2로 지정하면 첫 번째 title은 tt1로, 두 번째 title은 tt2로 변경된다.
        oldname의 필드 개수와, newname의 필드 개수는 동일해야 한다.
        존재하지 않는 필드에 대해서는 무시한다.

        :param oldname:
            이름을 바꿀 필드 이름의 리스트. 형식은 PutFieldText와 동일하게 "\x02"로 구분한다.

        :param newname:
            새로운 필드 이름의 리스트. oldname과 동일한 개수의 필드 이름을 "\x02"로 구분하여 지정한다.

        :return: None

        :example:
            >>> hwp.create_field("asdf")  # "asdf" 필드 생성
            >>> hwp.rename_field("asdf", "zxcv")  # asdf 필드명을 "zxcv"로 변경
            >>> hwp.put_field_text("zxcv", "Hello world!")  # zxcv 필드에 텍스트 삽입
        """
        return self.hwp.RenameField(oldname=oldname, newname=newname)
    

    def delete_all_fields(self:None): # 한글 문서 내부의 모든 누름틀 필드 제거
        '''
        한글문서 내부의 모든 누름틀 필드를 제거한다.
        누름틀 필드에 삽입된 텍스트는 남는다.
        '''
        start_pos = self.get_pos()
        ctrl = self.hwp.HeadCtrl
        while ctrl:
            if ctrl.CtrlID == "%clk":
                self.hwp.DeleteCtrl(ctrl)
            ctrl = ctrl.Next
        for field in self.get_field_list():
            self.rename_field(field, "")
        return self.set_pos(*start_pos)

# DataFrame 관련 메서드

    def put_DataFrame_text(self, field, text: Union[str, list, tuple, pd.Series] = "", idx=None): # 한글의 메일머지형태로 pd.DataFrame을 필드에 적습니다. ※column의 이름이 완전히 동일해야합니다.
        '한글의 메일머지형태로 pd.DataFrame을 필드에 적습니다. ※column의 이름이 완전히 동일해야합니다.'
        if isinstance(field, str) and (field.endswith(".xlsx") or field.endswith(".xls")):
            field = pd.read_excel(field)

        if isinstance(field, dict):  # dict 자료형의 경우에는 text를 생략하고
            field, text = list(zip(*list(field.items())))
            field_str = ""
            text_str = ""
            if isinstance(idx, int):
                for f_i, f in enumerate(field):
                    field_str += f"{f}{{{{{idx}}}}}\x02"
                    text_str += f"{text[f_i][idx]}\x02"
            else:
                if isinstance(text[0], (list, tuple)):
                    for f_i, f in enumerate(field):
                        for t_i, t in enumerate(text[f_i]):
                            field_str += f"{f}{{{{{t_i}}}}}\x02"
                            text_str += f"{t}\x02"
                elif isinstance(text[0], (str, int, float)):
                    for f_i, f in enumerate(field):
                        field_str += f"{f}\x02"
                    text_str = "\x02".join(text)

            self.hwp.PutFieldText(Field=field_str, Text=text_str)
            return

        if isinstance(field, str) and type(text) in (list, tuple, pd.Series):
            field = [f"{field}{{{{{i}}}}}" for i in range(len(text))]

        if isinstance(field, pd.Series):  # 필드명 리스트를 파라미터로 넣은 경우
            if not text:  # text 파라미터가 입력되지 않았다면
                text_str = "\x02".join([field[i] for i in field.index])
                field_str = "\x02".join([str(i) for i in field.index])  # \x02로 병합
                self.hwp.PutFieldText(Field=field_str, Text=text_str)
                return
            elif type(text) in [list, tuple, pd.Series]:  # 필드 텍스트를 리스트나 배열로 넣은 경우에도
                text = "\x02".join([str(i) for i in text])  # \x02로 병합
            else:
                raise IOError("text parameter required.")

        if isinstance(field, (list, tuple)):

            # field와 text가 [[field0:str, list[text:str]], [field1:str, list[text:str]]] 타입인 경우
            if not text and isinstance(field[0][0], (str, int, float)) and not isinstance(field[0][1], (str, int)) and len(field[0][1]) >= 1:
                text_str = ""
                field_str = "\x02".join(
                    [str(field[i][0]) + f"{{{{{j}}}}}" for j in range(len(field[0][1])) for i in range(len(field))])
                for i in range(len(field[0][1])):
                    text_str += "\x02".join([str(field[j][1][i]) for j in range(len(field))]) + "\x02"
                self.hwp.PutFieldText(Field=field_str, Text=text_str)
                return

            elif isinstance(field, (list, tuple, set)) and isinstance(text, (list, tuple, set)):
                # field와 text가 모두 배열로 만들어져 있는 경우
                field_str = "\x02".join([str(field[i]) for i in range(len(field))])
                text_str = "\x02".join([str(text[i]) for i in range(len(text))])
                self.hwp.PutFieldText(Field=field_str, Text=text_str)
                return
            else:
                # field와 text가 field타입 안에 [[field0:str, text0:str], [field1:str, text1:str]] 형태로 들어간 경우
                field_str = "\x02".join([str(field[i][0]) for i in range(len(field))])
                text_str = "\x02".join([str(field[i][1]) for i in range(len(field))])
                self.hwp.PutFieldText(Field=field_str, Text=text_str)
                return

        if isinstance(field, pd.DataFrame):
            if isinstance(field.columns, pd.core.indexes.range.RangeIndex):
                field = field.T
            text_str = ""
            if isinstance(idx, int):
                field_str = "\x02".join([str(i) + f"{{{{{idx}}}}}" for i in field])  # \x02로 병합
                text_str += "\x02".join([str(t) for t in field.iloc[idx]]) + "\x02"
            else:
                field_str = "\x02".join([str(i) + f"{{{{{j}}}}}" for j in range(len(field)) for i in field])  # \x02로 병합
                for i in range(len(field)):
                    text_str += "\x02".join([str(t) for t in field.iloc[i]]) + "\x02"
            self.hwp.PutFieldText(Field=field_str, Text=text_str)
            return

        if isinstance(text, pd.DataFrame):
            if not isinstance(text.columns, pd.core.indexes.range.RangeIndex):
                text = text.T
            text_str = ""
            if isinstance(idx, int):
                field_str = "\x02".join([i + f"{{{{{idx}}}}}" for i in field.split("\x02")])  # \x02로 병합
                text_str += "\x02".join([str(t) for t in text[idx]]) + "\x02"
            else:
                field_str = "\x02".join([str(i) + f"{{{{{j}}}}}" for i in field.split("\x02") for j in range(len(text.columns))])  # \x02로 병합
                for i in range(len(text)):
                    text_str += "\x02".join([str(t) for t in text.iloc[i]]) + "\x02"
            self.hwp.PutFieldText(Field=field_str, Text=text_str)
            return

        if isinstance(idx, int):
            self.hwp.PutFieldText(Field=field.replace("\x02", f"{{{{{idx}}}}}\x02") + f"{{{{{idx}}}}}", Text=text)
        else:
            self.hwp.PutFieldText(Field=field, Text=text)

    def get_DataFrame_Text(self, n="", cols=0): # Table을 DataFrame 형태로 가져옵니다.
        """
        (2024. 7. 26. xml파싱으로 방법 변경. 결국 기존 방법으로는 간단한 줄바꿈 이슈도 해결 못함.
                    startrow와 columns가 뭔가 중복되는 개념이어서, cols로 통일. 파괴적 업데이트라 죄송..)
        한/글 문서의 n번째 표를 판다스 데이터프레임으로 리턴하는 메서드.
        n을 넣지 않는 경우, 캐럿이 셀에 있다면 해당 표를 df로,
        캐럿이 표 밖에 있다면 첫 번째 표를 df로 리턴한다.
        
        ※주의 : 셀 병합이 있을 때 DataFrame을 제대로 불러오지 못한다.
        :return:
            pd.DataFrame
        :example:
            >>> from pyhwpx import Hwp
            >>>
            >>> hwp = Hwp()
            >>> df = hwp.table_to_df()  # 현재 캐럿이 들어가 있는 표 전체를 df로(1행을 df의 칼럼으로)
            >>> df = hwp.table_to_df(0, cols=2)  # 문서의 첫 번째 표를 df로(2번인덱스행(3행)을 칼럼명으로, 그 아래(4행부터)를 값으로)
            >>>
        """
        if self.SelectionMode != 19:
            start_pos = self.hwp.GetPos()
            ctrl = self.hwp.HeadCtrl
            if isinstance(n, type(ctrl)):
                # 정수인덱스 대신 ctrl 객체를 넣은 경우
                self.set_pos_by_set(n.GetAnchorPos(0))
                self.find_ctrl()
            elif n == "" and self.is_cell():
                self.TableCellBlock()
                self.TableColBegin()
                self.TableColPageUp()
            elif n == "" or isinstance(n, int):
                if n == "":
                    n = 0
                if n >= 0:
                    idx = 0
                else:
                    idx = -1
                    ctrl = self.hwp.LastCtrl

                while ctrl:
                    if ctrl.UserDesc == "표":
                        if n in (0, -1):
                            self.set_pos_by_set(ctrl.GetAnchorPos(0))
                            self.hwp.FindCtrl()
                            break
                        else:
                            if idx == n:
                                self.set_pos_by_set(ctrl.GetAnchorPos(0))
                                self.hwp.FindCtrl()
                                break
                            if n >= 0:
                                idx += 1
                            else:
                                idx -= 1
                    if n >= 0:
                        ctrl = ctrl.Next
                    else:
                        ctrl = ctrl.Prev

                try:
                    self.hwp.SetPosBySet(ctrl.GetAnchorPos(0))
                except AttributeError:
                    raise IndexError(f"해당 인덱스의 표가 존재하지 않습니다."
                                    f"현재 문서에는 표가 {abs(int(idx + 0.1))}개 존재합니다.")
                self.hwp.FindCtrl()
        else:
            selected_range = self.get_selected_range()
        
        xml_data = self.GetTextFile("HWPML2X", option="saveblock")
        root = ET.fromstring(xml_data)

        data = []

        for row in root.findall('.//ROW'):
            row_data = []
            for cell in row.findall('.//CELL'):
                cell_text = ''
                for text in cell.findall('.//TEXT'):
                    for char in text.findall('.//CHAR'):
                        cell_text += char.text
                    cell_text += "\r\n"
                if cell_text.endswith("\r\n"):
                    cell_text = cell_text[:-2]
                row_data.append(cell_text)
            data.append(row_data)
        
        if self.SelectionMode == 19:
            data = self.crop_data_from_selection(data, selected_range)
        
        if type(cols) == int:
            columns = data[cols]
            data = data[cols + 1:]
            df = pd.DataFrame(data, columns=columns)
        elif type(cols) in (list, tuple):
            df = pd.DataFrame(data, columns=cols)
        
        try:
            return df
        finally:
            if self.SelectionMode != 19:
                self.set_pos(*start_pos)

    def get_all_DataFrame(self):
        """
        모든 표의 데이터프레임을 얻습니다.
        여러 개일 경우 딕셔너리 {1: df1, 2: df2, ...} 형태로 리턴하고,
        하나일 경우에는 DataFrame을 그대로 리턴합니다.
        """
        self.data = []
        # 테이블의 첫 번째 컨트롤(HeadCtrl)로 시작
        ctrl = self.hwp.HeadCtrl
        # self.activate()

        # 테이블을 순차적으로 탐색하며 각 테이블 안으로 캐럿을 이동시키는 코드
        while ctrl:
            if ctrl.UserDesc == "표":  # "표"인 컨트롤을 찾음
                disp_val = ctrl.GetAnchorPos(0)  # 테이블의 앵커 위치를 얻음

                # 캐럿을 ParameterSet으로 얻은 위치로 이동
                success = self.set_pos_by_set(disp_val)  # 캐럿을 해당 위치로 이동시킴

                if success:
                    self.hwp.FindCtrl()  # 테이블 내의 컨트롤을 찾아 캐럿을 그 안으로 위치시킴
                    # pyautogui.press('enter')  # 'enter' 키를 눌러 작업을 수행
                    self.hwp.HAction.Run("ShapeObjTableSelCell")
                    self.data.append(self.get_DataFrame_Text())  # 추출한 DataFrame을 리스트에 추가
                # 다음 테이블로 이동
                ctrl = ctrl.Next  # 다음 컨트롤로 이동
            else:
                ctrl = ctrl.Next  # 표가 아닐 경우 다음 컨트롤로 이동

        # DataFrame이 하나일 경우 바로 반환
        if len(self.data) == 1:
            return self.data[0]

        # 여러 DataFrame일 경우 번호로 딕셔너리 반환 (1, 2, 3...)
        data_dict = {i + 1 : df for i, df in enumerate(self.data)}
        
        return data_dict  # 번호로 딕셔너리 반환


# 여러 한글창 조작하기

    def switch_to(self, num:int): 
        '''
        두개 이상의 문서를 다룰 때, 
        제어 한글창을 전환한다.
        0부터 시작한다.
        '''
        self.num = num
        return self.hwp.XHwpDocuments.Item(self.num).SetActive_XHwpDocument()

# 기타 기능
    

    def activate(self:None):
        '제어중인 한글창을 활성화한다'
        return self.hwp.XHwpDocuments.Item(0).SetActive_XHwpDocument()
    
    def insert_text(self, text : str): # 진짜 글자 삽입하는 메서드임
        """
        한/글 문서 내 캐럿 위치에 문자열을 삽입하는 메서드.
        :return:
            삽입 성공시 True, 실패시 False를 리턴함.
        :example:
            >>> from pyhwpx import Hwp
            >>> hwp = Hwp()
            >>> hwp.insert_text('Hello world!')
            >>> hwp.BreakPara()
        """
        param = self.hwp.HParameterSet.HInsertText
        self.hwp.HAction.GetDefault("InsertText", param.HSet)
        param.Text = text
        return self.hwp.HAction.Execute("InsertText", param.HSet)
    
    def to_PDF(self, path):
        """
        HWP 문서를 PDF로 저장하는 메서드.

        :param path: 저장할 PDF 파일의 경로 (절대경로 또는 상대경로)
        :return: 작업 실행 결과
        """
        # 상대경로를 절대경로로 변환
        if path.lower()[1] != ":":
            path = os.path.join(os.getcwd(), path)

        # FileSaveAsPdf 기본 설정 가져오기
        self.hwp.HAction.GetDefault("FileSaveAsPdf", self.hwp.HParameterSet.HFileOpenSave.HSet)
        
        # FileSaveAsPdf 파라미터 설정
        self.hwp.HParameterSet.HFileOpenSave.filename = path  # 저장할 PDF 파일 절대경로
        self.hwp.HParameterSet.HFileOpenSave.Format = "PDF"  # 파일 형식
        self.hwp.HParameterSet.HFileOpenSave.Attributes = 16384  # 속성 설정

        # 설정된 FileSaveAsPdf 작업 실행
        return self.hwp.HAction.Execute("FileSaveAsPdf", self.hwp.HParameterSet.HFileOpenSave.HSet)    
        
    def set_password(self, password: str):
        """
        HWP 문서에 파일 비밀번호를 설정하는 메서드.
        한글 2024이상 버젼에서 적용된다.
        
        Parameters:
            password (str): 설정할 비밀번호.
        """
        # FilePassword 작업 기본 설정 가져오기
        self.hwp.HAction.GetDefault("FilePassword", self.hwp.HParameterSet.HPassword.HSet)
        
        # FilePassword 파라미터 설정
        self.hwp.HParameterSet.HPassword.string = password   # 비밀번호 설정
        self.hwp.HParameterSet.HPassword.Level = 1       # 보안 수준 설정
        self.hwp.HParameterSet.HPassword.DialogType = 2 # 대화 상자 유형 설정
        
        # 설정된 FilePassword 작업 실행
        return self.hwp.HAction.Execute("FilePassword", self.hwp.HParameterSet.HPassword.HSet)

    

    def set_font_style(self, fontstyle: str = "굴림"):
        '블럭으로 잡은 글자의 글꼴을 변경한다.'
        
        # 문자 모양 설정을 초기화합니다.
        self.hwp.HAction.GetDefault("CharShape", self.hwp.HParameterSet.HCharShape.HSet)

        # 글꼴 설정
        self.hwp.HParameterSet.HCharShape.FaceNameUser = fontstyle
        self.hwp.HParameterSet.HCharShape.FontTypeUser = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FaceNameSymbol = fontstyle
        self.hwp.HParameterSet.HCharShape.FontTypeSymbol = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FaceNameOther = fontstyle
        self.hwp.HParameterSet.HCharShape.FontTypeOther = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FaceNameJapanese = fontstyle
        self.hwp.HParameterSet.HCharShape.FontTypeJapanese = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FaceNameHanja = fontstyle
        self.hwp.HParameterSet.HCharShape.FontTypeHanja = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FaceNameLatin = fontstyle
        self.hwp.HParameterSet.HCharShape.FontTypeLatin = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FaceNameHangul = fontstyle
        self.hwp.HParameterSet.HCharShape.FontTypeHangul = self.hwp.FontType("TTF")

        # 설정한 문자 모양을 실행하여 적용합니다.
        return self.hwp.HAction.Execute("CharShape", self.hwp.HParameterSet.HCharShape.HSet)

    def set_font_size(self, height : int = 10): 
        '블럭으로 잡은 글자의 크기를 변경한다'

        # 문자 모양 설정을 초기화합니다.
        self.hwp.HAction.GetDefault("CharShape", self.hwp.HParameterSet.HCharShape.HSet)

        # 글꼴 유형 및 크기 설정
        self.hwp.HParameterSet.HCharShape.FontTypeUser = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FontTypeSymbol = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FontTypeOther = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FontTypeJapanese = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FontTypeHanja = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FontTypeLatin = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FontTypeHangul = self.hwp.FontType("TTF")

        # 글꼴 크기 설정
        self.hwp.HParameterSet.HCharShape.Height = self.hwp.PointToHwpUnit(float(height))

        # 설정한 문자 모양을 실행하여 적용합니다.
        self.hwp.HAction.Execute("CharShape", self.hwp.HParameterSet.HCharShape.HSet)

        # 문자 모양 설정을 다시 초기화합니다.
        self.hwp.HAction.GetDefault("CharShape", self.hwp.HParameterSet.HCharShape.HSet)

        # 동일한 글꼴 유형 설정
        self.hwp.HParameterSet.HCharShape.FontTypeUser = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FontTypeSymbol = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FontTypeOther = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FontTypeJapanese = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FontTypeHanja = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FontTypeLatin = self.hwp.FontType("TTF")
        self.hwp.HParameterSet.HCharShape.FontTypeHangul = self.hwp.FontType("TTF")

        # 설정한 문자 모양을 실행하여 적용합니다.
        return self.hwp.HAction.Execute("CharShape", self.hwp.HParameterSet.HCharShape.HSet)


# 기타 부품들

    def key_indicator(self) -> tuple:
        """
        상태 바의 정보를 얻어온다.
        (캐럿이 표 안에 있을 때 셀의 주소를 얻어오는 거의 유일한 방법이다.)

        :return:
            튜플(succ, seccnt, secno, prnpageno, colno, line, pos, over, ctrlname)
            succ: 성공하면 True, 실패하면 False (항상 True임..)
            seccnt: 총 구역
            secno: 현재 구역
            prnpageno: 쪽
            colno: 단
            line: 줄
            pos: 칸
            over: 삽입모드 (True: 수정, False: 삽입)
            ctrlname: 캐럿이 위치한 곳의 컨트롤이름

        :example:
            >>> # 현재 셀 주소(표 안에 있을 때)
            >>> from pyhwpx import Hwp
            >>> hwp = Hwp()
            >>> hwp.KeyIndicator()[-1][1:].split(")")[0]
            "A1"
        """
        return self.hwp.KeyIndicator()

    def is_cell(self):
        """
        캐럿이 현재 표 안에 있는지 알려주는 메서드
        :return:
            표 안에 있으면 True, 그렇지 않으면 False를 리턴
        """
        if self.key_indicator()[-1].startswith("("):
            return True
        else:
            return False
        
    @property
    def SelectionMode(self):
        """
        현재 선택모드가 어떤 상태인지 리턴한다.
        :return:
        """
        return self.hwp.SelectionMode
    
    @property
    def HParameterSet(self):
        """
        한/글에서 실행되는 대부분의 액션에 필요한
        다양한 파라미터셋을 제공해주는 속성.
        사용법은 아래와 같다.

        >>> from pyhwpx import Hwp
        >>> hwp = Hwp()
        >>> pset = hwp.HParameterSet.HInsertText
        >>> pset.Text = "Hello world!"
        >>> hwp.HAction.Execute("InsertText", pset.HSet)

        :return:
        """
        return self.hwp.HParameterSet

    @property
    def HAction(self):
        """
        한/글의 액션을 설정하고 실행하기 위한 속성.
        GetDefalut, Execute, Run 등의 메서드를 가지고 있다.
        :return:
        """
        return self.hwp.HAction

    def goto_printpage(self, page_num: int = 1):
        """
        인쇄페이지 기준으로 해당 페이지로 이동
        1페이지의 page_num은 1이다.
        :param page_num: 이동할 페이지번호
        :return: 성공시 True, 실패시 False를 리턴
        """
        pset = self.hwp.HParameterSet.HGotoE
        self.hwp.HAction.GetDefault("Goto", pset.HSet)
        pset.HSet.SetItem("DialogResult", page_num)
        pset.SetSelectionIndex = 1
        return self.hwp.HAction.Execute("Goto", pset.HSet)
    
    def MovePageUp(self):
        """
        뒤 페이지의 시작으로 이동. 현재 탑레벨 리스트가 아니면 탑레벨 리스트로 빠져나온다.
        """
        cwd = self.get_pos()
        self.hwp.HAction.Run("MovePageUp")
        if self.get_pos()[0] != cwd[0] or self.get_pos()[1:] != cwd[1:]:
            return True
        else:
            return False
    
    def MovePageDown(self):
        """
        앞 페이지의 시작으로 이동. 현재 탑레벨 리스트가 아니면 탑레벨 리스트로 빠져나온다.
        """
        cwd = self.get_pos()
        self.hwp.HAction.Run("MovePageDown")
        if self.get_pos()[0] != cwd[0] or self.get_pos()[1:] != cwd[1:]:
            return True
        else:
            return False
    
    @property
    def current_printpage(self):
        """
        현재 쪽번호를 리턴.
        1페이지에 있다면 1을 리턴한다.
        새쪽번호가 적용되어 있다면
        수정된 쪽번호를 리턴한다.
        :return:
        """
        return self.hwp.XHwpDocuments.Active_XHwpDocument.XHwpDocumentInfo.CurrentPrintPage
    
    def mili_to_hwp_unit(self, mili):
        return self.hwp.MiliToHwpUnit(mili=mili)

    def get_pos(self) -> tuple[int]:
        """
        캐럿의 위치를 얻어온다.
        파라미터 중 리스트는, 문단과 컨트롤들이 연결된 한/글 문서 내 구조를 뜻한다.
        리스트 아이디는 문서 내 위치 정보 중 하나로서 SelectText에 넘겨줄 때 사용한다.
        (파이썬 자료형인 list가 아님)

        :return:
            (List, para, pos) 튜플.
            list: 캐럿이 위치한 문서 내 list ID(본문이 0)
            para: 캐럿이 위치한 문단 ID(0부터 시작)
            pos: 캐럿이 위치한 문단 내 글자 위치(0부터 시작)

        """
        return self.hwp.GetPos()
    
    def set_pos_by_set(self, disp_val):
        """
        캐럿을 ParameterSet으로 얻어지는 위치로 옮긴다.

        :param disp_val:
            캐럿을 옮길 위치에 대한 ParameterSet 정보

        :return:
            성공하면 True, 실패하면 False

        :example:
            >>> start_pos = hwp.GetPosBySet()  # 현재 위치를 저장하고,
            >>> hwp.set_pos_by_set(start_pos)  # 특정 작업 후에 저장위치로 재이동
        """
        return self.hwp.SetPosBySet(dispVal=disp_val)

    def get_cur_field_name(self, option=0):
        """
        현재 캐럿이 위치하는 곳의 필드이름을 구한다.
        이 함수를 통해 현재 필드가 셀필드인지 누름틀필드인지 구할 수 있다.
        참고로, 필드 좌측에 커서가 붙어있을 때는 이름을 구할 수 있지만,
        우측에 붙어 있을 때는 작동하지 않는다.
        GetFieldList()의 옵션 중에 hwpFieldSelection(=4)옵션은 사용하지 않는다.


        :param option:
            다음과 같은 옵션을 지정할 수 있다.
            0: 모두 off. 생략하면 0이 지정된다.
            1: 셀에 부여된 필드 리스트만을 구한다. hwpFieldClickHere와는 함께 지정할 수 없다.(hwpFieldCell)
            2: 누름틀에 부여된 필드 리스트만을 구한다. hwpFieldCell과는 함께 지정할 수 없다.(hwpFieldClickHere)

        :return:
            필드이름이 돌아온다.
            필드이름이 없는 경우 빈 문자열이 돌아온다.
        """
        return self.hwp.GetCurFieldName(option=option)
    
    def set_pos(self, list, para, pos):
        """
        캐럿을 문서 내 특정 위치로 옮긴다.
        지정된 위치로 캐럿을 옮겨준다.

        :param list:
            캐럿이 위치한 문서 내 list ID

        :param para:
            캐럿이 위치한 문단 ID. 음수거나, 범위를 넘어가면 문서의 시작으로 이동하며, pos는 무시한다.

        :param pos:
            캐럿이 위치한 문단 내 글자 위치. -1을 주면 해당문단의 끝으로 이동한다.
            단 para가 범위 밖일 경우 pos는 무시되고 문서의 시작으로 캐럿을 옮긴다.

        :return:
            성공하면 True, 실패하면 False
        """
        self.hwp.SetPos(List=list, Para=para, pos=pos)
        if (list, para) == self.get_pos()[:2]:
            return True
        else:
            return False
        
    def find_ctrl(self):
        return self.hwp.FindCtrl()

    def TableCellBlock(self):
        """
        셀 블록
        """
        # return self.hwp.HAction.Run("TableCellBlock")
        pset = self.HParameterSet.HInsertText
        self.HAction.GetDefault("TableCellBlock", pset.HSet)
        return self.HAction.Execute("TableCellBlock", pset.HSet)

    def TableColBegin(self):
        """
        셀 이동: 열 시작
        """
        return self.hwp.HAction.Run("TableColBegin")

    def TableColPageUp(self):
        """
        셀 이동: 페이지 업
        """
        return self.hwp.HAction.Run("TableColPageUp")

    def get_selected_range(self):
        """
        선택한 범위의 셀주소를
        리스트로 리턴함
        """
        if not self.is_cell():
            raise AttributeError("캐럿이 표 안에 있어야 합니다.")
        pset = self.HParameterSet.HFieldCtrl
        self.HAction.GetDefault("TableFormula", pset.HSet)
        return pset.Command[2:-1].split(",")

    def GetTextFile(self, format="UNICODE", option=""):
        
        return self.hwp.GetTextFile(Format=format, option=option)

    @staticmethod
    def cell_to_index(cell):
        """ 엑셀 셀 주소를 행과 열 인덱스로 변환"""
        column = ord(cell[0]) - ord('A')  # 열 인덱스 (0-based)
        row = int(cell[1:]) - 1  # 행 인덱스 (0-based)
        return row, column

    @staticmethod
    def crop_data_from_selection(data, selection):
        """ 리스트 a의 셀 주소를 바탕으로 데이터 범위를 추출"""
        if not selection:
            return []

        # 셀 주소를 행과 열 인덱스로 변환
        indices = [HWP.cell_to_index(cell) for cell in selection]

        # 범위 계산
        min_row = min(idx[0] for idx in indices)
        max_row = max(idx[0] for idx in indices)
        min_col = min(idx[1] for idx in indices)
        max_col = max(idx[1] for idx in indices)

        # 범위 추출
        result = []
        for row in range(min_row, max_row + 1):
            result.append(data[row][min_col:max_col + 1])

        return result

    def get_active_window_title(self): # 활성화된 window창의 제목을 리턴한다.
        hwnd = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(hwnd)
        return window_title
    
    
