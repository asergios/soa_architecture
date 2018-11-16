package es1819.stroam.notification.server;

import es1819.stroam.notification.server.utilities.GeneralUtilities;

import java.io.*;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.Properties;

public class Constants {

    public static String currentWorkingDirectoryPath;

    static {
        try {
            currentWorkingDirectoryPath =
                    new URI(GeneralUtilities.class.getProtectionDomain().getCodeSource().getLocation().getPath())
                            .getPath();

            //removes the last file/directory of path hierarchy and update the variable value
            int lastDirectoryPathHierarchyIndex = currentWorkingDirectoryPath
                    .lastIndexOf(System.getProperty("file.separator"));
            if(lastDirectoryPathHierarchyIndex > 0)
                currentWorkingDirectoryPath = currentWorkingDirectoryPath.substring(0, lastDirectoryPathHierarchyIndex); //update the variable value
        } catch (URISyntaxException ignored) {
            currentWorkingDirectoryPath = System.getProperty("user.dir");
        }
    }

    public static void loadConfigurationFile(File configurationFile) throws IOException {
        if(configurationFile == null) {
            loadDefaultSettings();
            return;
        }

        if(!configurationFile.canRead()) {
            loadDefaultSettings();
            throw new IOException("configuration file cannot be readed. Check read permissions");
        }

        if(configurationFile.isDirectory()) {
            File[] matchingFiles = configurationFile.listFiles(
                    (dir, name) -> name.matches(Constants.CONFIGURATION_FILE_NAME));

            if(matchingFiles != null && matchingFiles.length > 0)
                configurationFile = matchingFiles[0];
            else {
                loadDefaultSettings();
                return; //file not found
            }
        }

        BufferedReader fileReader = new BufferedReader(new FileReader(configurationFile));

        String readLine;
        while ((readLine = fileReader.readLine()) != null) {
            if(readLine.startsWith(CONFIGURATION_FILE_IGNORE_LINE_TAG))
                continue;

            String[] readLineKeyValue = readLine.split(" ");
            if(readLineKeyValue.length >= 2) {
                if(readLineKeyValue[0].isEmpty())
                    continue;

                if(runtimeProperties == null)
                    runtimeProperties = new Properties();
                runtimeProperties.setProperty(readLineKeyValue[0], readLineKeyValue[1]);
            }
        }
    }

    private static void loadDefaultSettings() {

    }

    //General constants/variables (from configuration file)
    public static Properties runtimeProperties = null;
    public static final String PROPERTY_DEBUG_MODE_NAME = "debug.mode";
    public static final String PROPERTY_BROKER_ADDRESS_NAME = "broker.address";

    //General constants
    public static final String CONFIGURATION_FILE_IGNORE_LINE_TAG = "#";
    public static final String CONFIGURATION_FILE_NAME = "nottheservice.conf";

    //Channel constants
    public static final String CHANNEL_SEPARATOR = "/";
    public static final String CHANNEL_SERVICE_PREFIX = "notTheService";
    public static final String CHANNEL_ALL_PREFIX = "#";
    public static final String CHANNEL_EMAIL_PREFIX = "email";
    public static final String CHANNEL_PHONE_PREFIX = "phone";
    public static final String CHANNEL_REQUEST_RESPONSE_PREFIX = "requestResponse";

    //Json constants
    public static final String JSON_REQUEST_ID_KEY = "requestId";
    public static final String JSON_EMAIL_SUBJECT_KEY = "subject";
    public static final String JSON_EMAIL_PHONE_BODY_KEY = "body";
    public static final String JSON_RESULT_CODE_KEY = "resultCode";
    public static final String JSON_ERROR_REASON_KEY = "reason";

    //Phone message constants
    public static final int PHONE_MESSAGE_MAX_CHARACTERS= 160;
}
