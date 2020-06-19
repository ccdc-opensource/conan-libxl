#include "libxl.h"

using namespace libxl;

int main()
{
    Book* book = xlCreateXMLBook();
    Sheet* sheet = book->addSheet("my");
    sheet->writeStr(5, 5, "Hello, World !");
    book->save("out.xlsx");
    book->release();

    return 0;
}