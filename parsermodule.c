#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>

int strpos(char *hay, char *needle, int offset) {
    char haystack[1024];  // I've been missing writing these buffers...
    strncpy(haystack, hay+offset, strlen(hay)-offset);
    haystack[strlen(hay)-offset] = '\0';
    char *p = strstr(haystack, needle);
    if (p) {
        if (p - haystack+offset + strlen(needle) + 1 >= strlen(hay)) {
            return -1;
        }
        return p - haystack+offset + strlen(needle) + 1;
    }
    return -1;
}

void substring(char s[], char sub[], int p, int l) {
    int c = 0;

    while (c < l) {
      sub[c] = s[p+c-1];
      c++;
    }
    sub[c] = '\0';
}

static PyObject *getLevel(PyObject *self, PyObject *args) {
    char *content;
    char id[37];
    char level[5];

    if (!PyArg_ParseTuple(args, "s", &content)) {
        return NULL;
    }
    int id_offset = strpos(content, "<var name=\"id\" value=\"", 0);
    substring(content, id, id_offset, 36);

    int level_offset = strpos(content, "<var name=\"level\" value=\"", 0);
    int length = strpos(content, "\"", level_offset) - level_offset - 1;
    substring(content, level, level_offset, length);

    return Py_BuildValue("ss", id, level);
}

static PyObject *getObjects(PyObject *self, PyObject *args) {
    char *content;
    if (!PyArg_ParseTuple(args, "s", &content)) {
        return NULL;
    }

    char result[1024] = "";
    int last = 0;
    char object[17];
    int object_offset = -1;
    int i = 0;
    do {
        object_offset = strpos(content, "<object name=\"", last);
        if (object_offset == -1) {
            break;
        }
        last = object_offset;
        substring(content, object, object_offset, 16);
        strcat(result, object);
        strcat(result, " ");
    } while (object_offset != -1);
    return Py_BuildValue("s", result);
}


static PyMethodDef moduleMethods[] = {
    {"get_level", getLevel, METH_VARARGS, NULL},
    {"get_objects", getObjects, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL} /* Sentinel */
};

static struct PyModuleDef parsermodule = {
    PyModuleDef_HEAD_INIT,
    "parsermodule",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    moduleMethods
};

PyMODINIT_FUNC PyInit_parsermodule(void) {
    return PyModule_Create(&parsermodule);
}