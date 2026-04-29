import flet as ft

def main(page: ft.Page):
    async def save_csv(e):
        try:
            file_picker = ft.FilePicker()
            page.overlay.append(file_picker)
            page.update()
            
            # Now await it
            path = await file_picker.save_file(dialog_title="Save", file_name="test.csv")
            print("Path:", path)
            page.window_close()
        except Exception as ex:
            print("Error:", ex)
    
    page.add(ft.ElevatedButton("Save", on_click=save_csv))

ft.app(target=main)
