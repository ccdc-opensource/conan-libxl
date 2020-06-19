#include "libxl.h"

using namespace libxl;

int main()
{
    Book* book = xlCreateXMLBook();
#ifdef _WIN32
    Sheet* sheet = book->addSheet(L"my");
    sheet->writeStr(5, 5, L"Hello, World !");
    book->save(L"out.xlsx");
#else
    Sheet* sheet = book->addSheet("my");
    sheet->writeStr(5, 5, "Hello, World !");
    book->save("out.xlsx");
#endif
    book->release();

    return 0;
}