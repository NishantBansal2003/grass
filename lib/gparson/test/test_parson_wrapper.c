/*****************************************************************************
 *
 * MODULE:       Grass JSON output interface
 *
 * PURPOSE:      Unit tests for gparson wrapper
 *
 * COPYRIGHT:    (C) 2010 by the GRASS Development Team
 *
 *               This program is free software under the GNU General Public
 *               License (>=v2). Read the file COPYING that comes with GRASS
 *               for details.
 *
 *****************************************************************************/

#include <string.h>
#include <grass/gis.h>
#include <grass/glocale.h>
#include <grass/parson.h>
#include <grass/gparson.h>
#include "test_gparson_lib.h"

static int test_gparson_wrapper(void);
/* ************************************************************************* */
/* Perform the JSON function wrapper unit tests *************************** */
/* ************************************************************************* */
int unit_test_parson_wrapper(void)
{
    int sum = 0;

    G_message(_("\n++ Running gparson wrapper unit tests ++"));

    sum += test_gparson_wrapper();

    if (sum > 0)
        G_warning(_("\n-- gparson wrapper unit tests failure --"));
    else
        G_message(
            _("\n-- gparson wrapper unit tests finished successfully --"));

    return sum;
}

/* *************************************************************** */
/* Test all implemented gparson wrapper functions **************** */
/* *************************************************************** */
int test_gparson_wrapper()
{
    int sum = 0;
    JSON_Value *value = NULL;
    JSON_Object *object = NULL;
    JSON_Array *array = NULL;
    char *serialized_string;

    G_message("\t * testing json object initialization\n");
    value = G_json_value_init_object();
    if (value == NULL) {
        G_warning("G_json_value_init_object failed!");
        sum++;
    }
    else {
        G_json_value_free(value);
    }

    G_message("\t * testing json array initialization\n");
    value = G_json_value_init_array();
    if (value == NULL) {
        G_warning("G_json_value_init_array failed!");
        sum++;
    }
    else {
        G_json_value_free(value);
    }

    G_message("\t * testing json object set and get functions\n");
    value = G_json_value_init_object();
    object = G_json_value_get_object(value);
    if (object == NULL) {
        G_warning("G_json_value_get_object failed!");
        sum++;
    }

    if (G_json_object_set_string(object, "key", "value") != JSONSuccess) {
        G_warning("G_json_object_set_string failed!");
        sum++;
    }

    const char *retrieved = G_json_object_get_string(object, "key");
    if (strcmp(retrieved, "value") != 0) {
        G_warning(
            "G_json_object_set_string or G_json_object_get_string failed!");
        sum++;
    }
    G_json_value_free(value);

    G_message("\t * Testing G_json_object_get_wrapping_value");
    value = G_json_value_init_object();
    object = G_json_value_get_object(value);
    if (G_json_object_get_wrapping_value(object) != value) {
        G_warning("G_json_object_get_wrapping_value failed!");
        sum++;
    }
    G_json_value_free(value);

    G_message("\t * testing json object set null\n");
    value = G_json_value_init_object();
    object = G_json_value_get_object(value);
    if (G_json_object_set_null(object, "null_key") != JSONSuccess) {
        G_warning("G_json_object_set_null failed!");
        sum++;
    }
    if (json_value_get_type(G_json_object_get_value(object, "null_key")) !=
        JSONNull) {
        G_warning("G_json_object_set_null or retrieval failed!");
        sum++;
    }
    G_json_value_free(value);

    G_message("\t * testing json object get array\n");
    value = G_json_value_init_object();
    object = G_json_value_get_object(value);
    if (G_json_object_set_value(object, "array", G_json_value_init_array()) !=
        JSONSuccess) {
        G_warning("G_json_object_set_value for array failed!");
        sum++;
    }
    array = G_json_object_get_array(object, "array");
    if (!array) {
        G_warning("G_json_object_get_array failed!");
        sum++;
    }
    G_json_value_free(value);

    G_message("\t * testing json object get object\n");
    value = G_json_value_init_object();
    object = G_json_value_get_object(value);
    if (G_json_object_set_value(object, "nested", G_json_value_init_object()) !=
        JSONSuccess) {
        G_warning("G_json_object_set_value for nested object failed!");
        sum++;
    }
    JSON_Object *nested_object = G_json_object_get_object(object, "nested");
    if (!nested_object) {
        G_warning("G_json_object_get_object failed!");
        sum++;
    }
    G_json_value_free(value);

    G_message("\t * testing json array append value\n");
    value = G_json_value_init_array();
    array = G_json_array(value);
    if (G_json_array_append_value(array, G_json_value_init_object()) !=
        JSONSuccess) {
        G_warning("G_json_array_append_value failed!");
        sum++;
    }
    G_json_value_free(value);

    G_message("\t * testing json array append number\n");
    value = G_json_value_init_array();
    array = G_json_array(value);
    if (G_json_array_append_number(array, 123.45) != JSONSuccess) {
        G_warning("G_json_array_append_number failed!");
        sum++;
    }
    if (G_json_array_get_number(array, 0) != 123.45) {
        G_warning("G_json_array_append_number or retrieval failed!");
        sum++;
    }
    G_json_value_free(value);

    G_message("\t * testing json array append boolean\n");
    value = G_json_value_init_array();
    array = G_json_array(value);
    if (G_json_array_append_boolean(array, 1) != JSONSuccess) {
        G_warning("G_json_array_append_boolean failed!");
        sum++;
    }
    if (G_json_array_get_boolean(array, 0) != 1) {
        G_warning("G_json_array_append_boolean or retrieval failed!");
        sum++;
    }
    G_json_value_free(value);

    G_message("\t * testing json array append null\n");
    value = G_json_value_init_array();
    array = G_json_array(value);
    if (G_json_array_append_null(array) != JSONSuccess) {
        G_warning("G_json_array_append_null failed!");
        sum++;
    }
    if (json_value_get_type(G_json_array_get_value(array, 0)) != JSONNull) {
        G_warning("G_json_array_append_null or retrieval failed!");
        sum++;
    }
    G_json_value_free(value);

    G_message("\t * testing json array append string\n");
    value = G_json_value_init_array();
    array = G_json_array(value);
    if (G_json_array_append_string(array, "array_string") != JSONSuccess) {
        G_warning("G_json_array_append_null failed!");
        sum++;
    }
    if (strcmp(G_json_array_get_string(array, 0), "array_string") != 0) {
        G_warning("G_json_array_append_null or retrieval failed!");
        sum++;
    }
    G_json_value_free(value);

    G_message("\t * testing json object set and get number functions\n");
    value = G_json_value_init_object();
    object = G_json_value_get_object(value);
    if (G_json_object_set_number(object, "number_key", 42.0) != JSONSuccess) {
        G_warning("G_json_object_set_number failed!");
        sum++;
    }
    double number = G_json_object_get_number(object, "number_key");
    if (number != 42.0) {
        G_warning(
            "G_json_object_set_number or G_json_object_get_number failed!");
        sum++;
    }
    G_json_value_free(value);

    G_message("\t * testing json object set and get boolean functions\n");
    value = G_json_value_init_object();
    object = G_json_value_get_object(value);
    if (G_json_object_set_boolean(object, "boolean_key", 1) != JSONSuccess) {
        G_warning("G_json_object_set_boolean failed!");
        sum++;
    }
    int booleanValue = G_json_object_get_boolean(object, "boolean_key");
    if (booleanValue != 1) {
        G_warning(
            "G_json_object_set_boolean or G_json_object_get_boolean failed!");
        sum++;
    }
    G_json_value_free(value);

    G_message("\t * testing JSON serialization\n");
    value = G_json_value_init_object();
    object = G_json_value_get_object(value);
    G_json_object_set_string(object, "key", "value");

    serialized_string = G_json_serialize_to_string_pretty(value);
    if (!serialized_string || strstr(serialized_string, "value") == NULL) {
        G_warning("Error in JSON serialization");
        sum++;
    }

    G_json_free_serialized_string(serialized_string);
    G_json_value_free(value);

    return sum;
}
